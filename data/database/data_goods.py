# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.goods import Goods

logger = LoggerUtils('data.goods').logger


def goods_by_id(connection, id):
    goods = None
    try:
        sql = config.get("sql", "sql_goods_by_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            result = cursor.fetchone()
            if result is not None:
                goods = Goods()
                goods.id = result["id"]
                goods.name = result["name"]
                goods.create_time = result["create_time"]
                goods.amount = float(result["amount"])
                goods.vip_days = result["vip_days"]
                goods.status = result["status"]
    except:
        logger.exception(traceback.format_exc())
    return goods


def goods_list(connection):
    goods_list = []
    try:
        sql = config.get("sql", "sql_goods_list")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                goods = Goods()
                goods.id = result["id"]
                goods.name = result["name"]
                goods.create_time = result["create_time"]
                goods.amount = float(result["amount"])
                goods.vip_days = result["vip_days"]
                goods.status = result["status"]
                goods_list.append(json.dumps(goods.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return goods_list
