# coding=utf-8
import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils
from pycore.utils.stringutils import StringUtils

from data.database import data_account, data_goods, data_gold, data_order
from mode import pay_type
from mode.order import Order
from utils import project_utils

logger = LoggerUtils('api.order').logger


def create():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        data = request.form
        connection = None
        try:
            connection = mysql_connection.get_conn()
            account = data_account.query_account_by_id(connection, account_id)
            if account is not None:
                goods_id = data["goods_id"]
                goods = data_goods.goods_by_id(connection, goods_id)
                if account.gold >= goods.amount:
                    data_account.update_gold(connection, -goods.amount, account.id)
                    data_gold.create_gold(connection, 4, 0, account.id, -goods.amount)
                    order_no = StringUtils.randomStr(32)
                    while data_order.order_by_order_no(connection, order_no) is not None:
                        order_no = StringUtils.randomStr(32)
                    order = Order()
                    order.order_no = order_no
                    order.create_time = int(time.time())
                    order.account_id = account.id
                    order.amount = goods.amount
                    order.goods_id = goods.id
                    order.pay_type = pay_type.OFFLINE
                    order.details = goods.name
                    data_order.create_order(connection, order)
                    data_order.pay_order(connection, order.order_no)
                    result = '{"state":0}'

                    # 直接使用卡密
                    # create_time = int(time.time())
                    # goods = data_goods.goods_by_id(connection, order.goods_id)
                    # last_end_time = data_vip.vip_end_time(connection, account_id)
                    # if last_end_time > create_time:
                    #     start_time = last_end_time
                    # else:
                    #     start_time = create_time
                    # end_time = goods.vip_days * 86400 + start_time
                    # vip = Vip()
                    # vip.account_id = account_id
                    # vip.create_time = create_time
                    # vip.start_time = start_time
                    # vip.end_time = end_time
                    # vip.order_no = order_no
                    # vip.operation_account = account_id
                    # data_vip.create_vip(connection, vip)
                    # data_order.use_order(connection, order_no)
                else:
                    result = '{"state":3}'
        except:
            logger.exception(traceback.format_exc())
        finally:
            if connection is not None:
                connection.close()
    else:
        result = '{"state":%d}' % code
    return result


def list():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        data = request.form
        connection = None
        page = int(data["page"])
        try:
            connection = mysql_connection.get_conn()
            orders = data_order.order_list(connection, account_id, page)
            result = '{"state":0, "data":[%s]}' % ",".join(orders)
        except:
            logger.exception(traceback.format_exc())
        finally:
            if connection is not None:
                connection.close()
    else:
        result = '{"state":%d}' % code
    return result
