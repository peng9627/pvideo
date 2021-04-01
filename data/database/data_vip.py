# coding=utf-8
import json
import time
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.vip import Vip

logger = LoggerUtils("data.vip").logger


def is_vip(connection, account_id):
    try:
        this_time = int(time.time())
        sql = config.get("sql", "sql_is_vip") % (this_time, this_time, account_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())


def end_time(connection, account_id):
    result = 0
    try:
        sql = config.get("sql", "sql_vip_end_time") % account_id
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchone()
            if r is not None:
                result = r["result"]
    except:
        logger.exception(traceback.format_exc())
    return result


def create(connection, vip):
    try:
        sql = config.get("sql", "sql_create_vip")
        with connection.cursor() as cursor:
            cursor.execute(sql, (
                vip.account_id, vip.create_time, vip.start_time, vip.end_time, vip.order_no, vip.operation_account))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def use_history(connection, user_id, page, page_size=20):
    vips = []
    try:
        sql = config.get("sql", "sql_vip_use_history")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, (page - 1) * page_size, page_size))
            r = cursor.fetchall()
            for result in r:
                vip = Vip()
                vip.order_no = result["order_no"]
                vip.create_time = result["create_time"]
                vip.account_id = result["account_id"]
                vips.append(json.dumps(vip.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return vips
