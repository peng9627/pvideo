import traceback

from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_vip_video

logger = LoggerUtils('api.vip_video').logger


def query():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        videos = data_vip_video.query(connection)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
