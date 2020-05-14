# coding=utf-8
import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_goods, data_order, data_vip
from mode.vip import Vip

logger = LoggerUtils('api.vip').logger


def use_code():
    result = '{"state":-1}'
    data = request.form
    if "HTTP_AUTH" in request.headers.environ:
        sessionid = request.headers.environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        if not redis.exists(sessionid):
            result = '{"state":2}'
        else:
            sessions = redis.getobj(sessionid)
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                order_no = data["code"]
                order = data_order.order_by_order_no(connection, order_no)
                if order is None:
                    result = '{"state":3}'
                elif order.status == 2:
                    result = '{"state":4}'
                else:
                    create_time = int(time.time())
                    goods = data_goods.goods_by_id(connection, order.goods_id)
                    last_end_time = data_vip.vip_end_time(connection, account_id)
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
                    data_vip.create_vip(connection, vip)
                    data_order.use_order(connection, order_no)
                    result = '{"state":0}'
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'
    return result


def use_history():
    result = '{"state":-1}'
    data = request.form
    if "HTTP_AUTH" in request.headers.environ:
        sessionid = request.headers.environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        if not redis.exists(sessionid):
            result = '{"state":2}'
        else:
            sessions = redis.getobj(sessionid)
            account_id = sessions["id"]
            connection = None
            page = int(data["page"])
            try:
                connection = mysql_connection.get_conn()
                vips = data_vip.use_history(connection, account_id, page)
                result = '{"state":0, "data":[%s]}' % ",".join(vips)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'
    return result
