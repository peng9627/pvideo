# coding=utf-8
import time
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.gold").logger


def create_gold(connection, type, source, user_id, gold):
    from data.database import data_account
    try:
        account = data_account.query_account_by_id(connection, user_id)
        sql = config.get("sql", "sql_create_gold") % (type, source, user_id, gold, account.gold, int(time.time()))
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def gold_sum(connection, id, type, time_stamp):
    result = 0
    try:
        sql = config.get("sql", "sql_gold_sum")
        with connection.cursor() as cursor:
            cursor.execute(sql, (id, type, time_stamp))
            r = cursor.fetchone()
            if r is not None:
                result = r["result"]
                if result is None:
                    result = 0
    except:
        logger.exception(traceback.format_exc())
    return result
