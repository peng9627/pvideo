# coding=utf-8
import json
import time
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.order import Order

logger = LoggerUtils('data.order').logger


def create(connection, order):
    try:
        sql = config.get("sql", "sql_create_order")
        with connection.cursor() as cursor:
            cursor.execute(sql, (
                order.order_no, order.create_time, order.account_id, order.amount, order.goods_id, order.pay_type,
                order.details))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def pay(connection, order_no):
    try:
        sql = config.get("sql", "sql_pay_order")
        with connection.cursor() as cursor:
            cursor.execute(sql, (1, int(time.time()), order_no))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def use(connection, order_no):
    try:
        sql = config.get("sql", "sql_pay_order")
        with connection.cursor() as cursor:
            cursor.execute(sql, (2, int(time.time()), order_no))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def by_order_no(connection, order_no):
    order = None
    try:
        sql = config.get("sql", "sql_order_by_no")
        with connection.cursor() as cursor:
            cursor.execute(sql, order_no)
            result = cursor.fetchone()
            if result is not None:
                order = Order()
                order.goods_id = result["goods_id"]
                order.status = result["status"]
    except:
        logger.exception(traceback.format_exc())
    return order


def list(connection, user_id, page, page_size=20):
    orders = []
    try:
        sql = config.get("sql", "sql_order_list")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, (page - 1) * page_size, page_size))
            r = cursor.fetchall()
            for result in r:
                order = Order()
                order.order_no = result["order_no"]
                order.create_time = result["create_time"]
                order.status = result["status"]
                order.details = result["details"]
                orders.append(json.dumps(order.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return orders


def change_out_order_no(connection, out_order_no):
    try:
        sql = config.get("sql", "sql_change_out_order_no")
        with connection.cursor() as cursor:
            cursor.execute(sql, out_order_no)
            connection.commit()
    except:
        logger.exception(traceback.format_exc())
