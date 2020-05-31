# coding=utf-8
import traceback

from pycore.data.database import mysql_connection
from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils('data.delete_room').logger


def delete_room_list(connection):
    close = connection is None
    delete_rooms = []
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_delete_room_list")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                delete_rooms.append(result["room_name"])
    except:
        if close and connection is not None:
            connection.rollback()
        logger.exception(traceback.format_exc())
    finally:
        if close and connection is not None:
            connection.close()
    return delete_rooms
