import json
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_notice

logger = LoggerUtils('api.notice').logger


def query():
    result = '{"state":-1}'
    data = request.form
    type = data["type"]
    connection = None
    try:
        connection = mysql_connection.get_conn()
        notice = data_notice.query(connection, type)
        if notice is not None:
            result = '{"state":0, "data":%s}' % json.dumps(notice.__dict__)
        else:
            result = '{"state":1}'
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
