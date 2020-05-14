# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.vip_video_url import VipVideoUrl

logger = LoggerUtils("data_vip_video_url").logger


def query(connection):
    urls = []
    try:
        sql = config.get("sql", "sql_vip_video_url")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                a = VipVideoUrl()
                a.id = result["id"]
                a.address = result["address"]
                a.name = result["name"]
                urls.append(json.dumps(a.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return urls
