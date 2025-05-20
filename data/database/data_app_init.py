# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.app_init").logger


def init(connection, create_time, user_id, device, ip, platform):
    try:
        sql = config.get("sql", "sql_create_app_init")
        with connection.cursor() as cursor:
            cursor.execute(sql, (create_time, user_id, device, ip, platform))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())
