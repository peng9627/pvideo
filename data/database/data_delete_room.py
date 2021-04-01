# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils('data.delete_room').logger


def delete(connection):
    delete_rooms = []
    try:
        sql = config.get("sql", "sql_delete_room_list")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                delete_rooms.append(result["room_name"])
    except:
        logger.exception(traceback.format_exc())
    return delete_rooms
