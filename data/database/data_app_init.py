# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.app_init").logger


def init(connection, create_time, user_id, device, ip):
    try:
        sql = config.get("sql", "sql_create_app_init")
        with connection.cursor() as cursor:
            cursor.execute(sql, (create_time, user_id, device, ip))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def exist(connection, movie):
    try:
        sql = config.get("sql", "sql_movie_exist")
        with connection.cursor() as cursor:
            cursor.execute(sql, (movie.title, movie.year, movie.type))
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False
