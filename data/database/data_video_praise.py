# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.praise").logger


def create(connection, user_video):
    result = 0
    try:
        sql = config.get("sql", "sql_add_video_praise")
        with connection.cursor() as cursor:
            result = cursor.execute(sql, user_video)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())
    return result


def cancel(connection, user_video):
    result = 0
    try:
        sql = config.get("sql", "sql_cancel_video_praise")
        with connection.cursor() as cursor:
            result = cursor.execute(sql, user_video)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())
    return result


def exist(connection, user_video):
    try:
        sql = config.get("sql", "sql_exist_video_praise")
        with connection.cursor() as cursor:
            cursor.execute(sql, user_video)
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False


def count(connection, user_video):
    result = 0
    try:
        sql = config.get("sql", "sql_video_praise_count")
        with connection.cursor() as cursor:
            cursor.execute(sql, "%" + user_video + "%")
            result = cursor.fetchone()
            result = result["result"]
    except:
        logger.exception(traceback.format_exc())
    return result
