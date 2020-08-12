# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.video_type import VideoType

logger = LoggerUtils("data.video_type").logger


def query_types(connection):
    video_types = []
    try:
        sql = config.get("sql", "sql_video_types")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                v = VideoType()
                v.id = result["id"]
                v.title = result["title"]
                v.pid = result["pid"]
                v.pic = result["pic"]
                video_types.append(json.dumps(v.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return video_types
