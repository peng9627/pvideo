# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.vip_video import VipVideo

logger = LoggerUtils("data_vip_video").logger


def query(connection):
    videos = []
    try:
        sql = config.get("sql", "sql_vip_video")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                a = VipVideo()
                a.id = result["id"]
                a.pic = result["pic"]
                a.address = result["address"]
                a.name = result["name"]
                videos.append(json.dumps(a.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return videos
