# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.tv_url import TvUrl

logger = LoggerUtils("data_tv_url").logger


def query(connection):
    tvs = []
    try:
        sql = config.get("sql", "sql_tv_url")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                a = TvUrl()
                a.id = result["id"]
                a.pic = result["pic"]
                a.address = result["address"]
                a.name = result["name"]
                tvs.append(json.dumps(a.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return tvs
