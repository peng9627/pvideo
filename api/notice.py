import json
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_notice
from utils import project_utils

logger = LoggerUtils('api.notice').logger


def query():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            type = data['type']
            connection = None
            try:
                connection = mysql_connection.get_conn()
                notice = data_notice.query(connection, type)
                if notice is not None:
                    result = '{"state":0, "data":%s}' % json.dumps(notice.__dict__)
                else:
                    result = '{"state":3}'
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result
