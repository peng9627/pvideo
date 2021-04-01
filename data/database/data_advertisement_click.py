# coding=utf-8
import time
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.advertisement").logger


def click(connection, ad_id, userId):
    try:
        sql = config.get("sql", "sql_advertisement_clicked_add") % (ad_id, userId, int(time.time()))
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())
