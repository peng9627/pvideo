# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.play_details").logger


def create(connection, video_id, create_time):
    try:
        if not exist(connection, video_id, create_time):
            sql = config.get("sql", "sql_create_play_details")
            with connection.cursor() as cursor:
                cursor.execute(sql, (video_id, create_time))
                connection.commit()
        else:
            sql = config.get("sql", "sql_play_details_add_count")
            with connection.cursor() as cursor:
                cursor.execute(sql, (video_id, create_time))
                connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def exist(connection, video_id, create_time):
    try:
        sql = config.get("sql", "sql_play_details_exist")
        with connection.cursor() as cursor:
            cursor.execute(sql, (video_id, create_time))
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False
