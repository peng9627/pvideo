# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.recommend import Recommend

logger = LoggerUtils("data_recommend").logger


def query(connection):
    recommends = []
    try:
        sql = config.get("sql", "sql_recommend")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                a = Recommend()
                a.id = result["id"]
                a.pic = result["pic"]
                a.address = result["address"]
                a.name = result["name"]
                a.desc = result["desc"]
                recommends.append(json.dumps(a.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return recommends
