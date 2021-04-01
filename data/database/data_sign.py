# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.sign").logger


def sign(connection, user_id, create_time, gold):
    try:
        if not exist(connection, user_id, create_time):
            sql = config.get("sql", "sql_create_sign")
            with connection.cursor() as cursor:
                cursor.execute(sql, (create_time, user_id, gold))
                connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def exist(connection, user_id, create_time):
    try:
        sql = config.get("sql", "sql_sign_exist")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, create_time))
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False


def by_time(connection, user_id, create_time):
    gold = 0
    try:
        sql = config.get("sql", "sql_sign_by_time")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, create_time))
            result = cursor.fetchone()
            if result is not None:
                gold = result['gold']
    except:
        logger.exception(traceback.format_exc())
    return gold
