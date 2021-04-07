# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.video_real_addr").logger


def add(connection, create_time, url_id, address, rel_address):
    try:
        if not exist(connection, url_id, address):
            sql = config.get("sql", "sql_add_video_real_addr")
            with connection.cursor() as cursor:
                cursor.execute(sql, (create_time, url_id, address, rel_address))
                connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def exist(connection, url_id, address):
    try:
        sql = config.get("sql", "sql_video_real_addr_exist")
        with connection.cursor() as cursor:
            cursor.execute(sql, (url_id, address))
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False


def query(connection, address):
    real_addrs = []
    try:
        with connection.cursor() as cursor:
            sql = config.get("sql", "sql_query_video_real_addr")
            cursor.execute(sql, address)
            r = cursor.fetchall()
            for result in r:
                real_addrs.append({'url_id': result["url_id"], 'rel_address': result["rel_address"]})
    except:
        logger.exception(traceback.format_exc())
    return real_addrs
