import traceback

from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_vip_video_url

logger = LoggerUtils('api.vip_video_url').logger


def query():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        urls = data_vip_video_url.query(connection)
        result = '{"state":0, "data":[%s]}' % ",".join(urls)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
