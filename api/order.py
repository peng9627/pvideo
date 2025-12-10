# coding=utf-8
import json
import time
import traceback

import requests
from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import config
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils
from pycore.utils.stringutils import StringUtils

from data.database import data_account, data_goods, data_gold, data_order, data_vip, data_recharge_config
from mode import pay_type
from mode.order import Order
from mode.vip import Vip
from utils import project_utils

logger = LoggerUtils('api.order').logger

recharge_key = 'XXK8IMEG1QXLQZGB3RKXFLYYYZ8IAFYFOIIMDYVDZ6LJWNAUKZHCFBVYN6UO49RFMOOZZFY31WYCC9JH3G1Y5BJO2GJARKSEXGMNSPDEKJYVPG7ISKACPIRQJGI5K1S0'


def create():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    account = data_account.query_by_id(connection, account_id)
                    if account is not None:
                        goods_id = data["goods_id"]
                        goods = data_goods.by_id(connection, goods_id)
                        if account.gold >= goods.amount:
                            data_account.update_gold(connection, -goods.amount, account.id)
                            data_gold.create(connection, 4, 0, account.id, -goods.amount)
                            order_no = StringUtils.randomStr(32)
                            while data_order.by_order_no(connection, order_no) is not None:
                                order_no = StringUtils.randomStr(32)
                            order = Order()
                            order.order_no = order_no
                            order.create_time = int(time.time())
                            order.account_id = account.id
                            order.amount = goods.amount
                            order.goods_id = goods.id
                            order.pay_type = pay_type.OFFLINE
                            order.details = goods.name
                            data_order.create(connection, order)
                            data_order.pay(connection, order.order_no)
                            result = '{"state":0}'
                            if config.get("server", "use_order") == "True":
                                # 直接使用卡密
                                create_time = int(time.time())
                                goods = data_goods.by_id(connection, order.goods_id)
                                last_end_time = data_vip.end_time(connection, account_id)
                                if last_end_time > create_time:
                                    start_time = last_end_time
                                else:
                                    start_time = create_time
                                end_time = goods.vip_days * 86400 + start_time
                                vip = Vip()
                                vip.account_id = account_id
                                vip.create_time = create_time
                                vip.start_time = start_time
                                vip.end_time = end_time
                                vip.order_no = order_no
                                vip.operation_account = account_id
                                data_vip.create(connection, vip)
                                data_order.use(connection, order_no)
                        else:
                            result = '{"state":3}'
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def recharge():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    account = data_account.query_by_id(connection, account_id)
                    if account is not None:
                        config_id = data["config_id"]
                        recharge_config = data_recharge_config.by_id(connection, config_id)
                        order_no = StringUtils.randomStr(32)
                        while data_order.by_order_no(connection, order_no) is not None:
                            order_no = StringUtils.randomStr(32)
                        order = Order()
                        order.order_no = order_no
                        order.create_time = int(time.time())
                        order.account_id = account.id
                        order.amount = recharge_config.amount
                        order.goods_id = recharge_config.id
                        order.pay_type = pay_type.ALIPAY
                        order.details = recharge_config.name
                        data_order.create(connection, order)

                        recharge_param = {}
                        recharge_param["mchId"] = 251
                        recharge_param["productId"] = 813
                        recharge_param["mchOrderNo"] = order_no
                        recharge_param["amount"] = recharge_config.amount
                        recharge_param["notifyUrl"] = 'http://127.0.0.1:5555/order/pay'
                        # recharge_param["returnUrl"] = ''

                        sign_str = 'amount=' + str(
                            recharge_config.amount) + '&mchId=251&mchOrderNo=' + order_no + '&notifyUrl=' + \
                                   recharge_param["notifyUrl"] + '&productId=813' + '&key=' + recharge_key
                        recharge_param["sign"] = StringUtils.md5(sign_str)

                        res = requests.post('http://pay.bafun.sbs/api/pay/create_order',
                                            json=json.dumps(recharge_param)).json()
                        logger.info('recharge_res:' + json.dumps(res))
                        if res["retCode"] == 'SUCCESS':
                            data_order.change_out_order_no(connection, res["payOrderId"])
                            return '{"state":0,"data":%s}' % json.dumps(res['payParams'])
                        result = '{"state":3}'
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def pay():
    data = request.json
    out_order_no = data["payOrderId"]
    mchId = data["mchId"]
    productId = data["productId"]
    mchOrderNo = data["mchOrderNo"]
    amount = data["amount"]
    status = data["status"]
    paySuccTime = data["paySuccTime"]
    sign = data["sign"]

    sign_str = 'amount=' + str(amount) + '&mchId=' + str(mchId) + '&mchOrderNo=' + str(
        mchOrderNo) + '&payOrderId=' + str(out_order_no) + '&paySuccTime=' + str(paySuccTime) + '&productId=' + str(
        productId) + '&status=' + str(status) + '&key=' + recharge_key
    if sign != StringUtils.md5(sign_str):
        return 'False'

    connection = None
    try:
        connection = mysql_connection.get_conn()
        order = data_order.by_order_no(connection, mchOrderNo)
        if order is not None:
            recharge_config = data_recharge_config.by_id(connection, order.goods_id)
            last_end_time = data_vip.end_time(connection, order.account_id)
            create_time = int(time.time())
            if last_end_time > create_time:
                start_time = last_end_time
            else:
                start_time = create_time
            end_time = recharge_config.vip_days * 86400 + start_time
            vip = Vip()
            vip.account_id = order.account_id
            vip.create_time = create_time
            vip.start_time = start_time
            vip.end_time = end_time
            vip.order_no = mchOrderNo
            vip.operation_account = order.account_id
            data_vip.create(connection, vip)
            data_order.use(connection, mchOrderNo)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()


def list():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                connection = None
                page = int(data["page"])
                try:
                    connection = mysql_connection.get_conn()
                    orders = data_order.list(connection, account_id, page)
                    result = '{"state":0, "data":[%s]}' % ",".join(orders)
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result
