import traceback

from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_tv_url

logger = LoggerUtils('api.tv_url').logger


def query():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        tvs = data_tv_url.query(connection)
        result = '{"state":0, "data":[%s]}' % ",".join(tvs)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
