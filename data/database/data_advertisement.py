# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.advertisement import Advertisement

logger = LoggerUtils("data.advertisement").logger


def query_advertisements(connection, where):
    advertisements = []
    try:
        sql = config.get("sql", "sql_advertisement")
        with connection.cursor() as cursor:
            cursor.execute(sql, where)
            r = cursor.fetchall()
            for result in r:
                a = Advertisement()
                a.id = result["id"]
                a.type = result["type"]
                a.pic = result["pic"]
                a.address = result["address"]
                advertisements.append(json.dumps(a.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return advertisements


def add_count(connection, id):
    try:
        sql = config.get("sql", "sql_advertisement_add_count") % id
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())
