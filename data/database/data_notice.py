# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.notice import Notice

logger = LoggerUtils("data_notice").logger


def query(connection, type):
    notice = None
    try:
        sql = config.get("sql", "sql_notice_by_type")
        with connection.cursor() as cursor:
            cursor.execute(sql, type)
            result = cursor.fetchone()
            if result is not None:
                notice = Notice()
                notice.title = result["title"]
                notice.content = result["content"]
    except:
        logger.exception(traceback.format_exc())
    return notice
