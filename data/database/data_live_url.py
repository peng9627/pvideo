# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.live_url import LiveUrl

logger = LoggerUtils("data.live_url").logger


def query(connection):
    urls = []
    try:
        sql = config.get("sql", "sql_live_url")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                a = LiveUrl()
                a.id = result["id"]
                a.address = result["address"]
                a.name = result["name"]
                urls.append(a)
    except:
        logger.exception(traceback.format_exc())
    return urls
