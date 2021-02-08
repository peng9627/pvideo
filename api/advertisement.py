import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_advertisement, data_advertisement_click
from utils import project_utils, aes_utils

logger = LoggerUtils('api.advertisement').logger


def query():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            where = data["where"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                advertisement = data_advertisement.query_advertisements(connection, where)
                result = '{"state":0, "data":[%s]}' % ",".join(advertisement)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def click():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            id = data["id"]
            connection = None
            account_id = 0
            try:
                connection = mysql_connection.get_conn()
                data_advertisement.add_count(connection, id)
                code, sessions = project_utils.get_auth(request.headers.environ)
                if 0 == code:
                    account_id = sessions["id"]
                data_advertisement_click.create_click(connection, id, account_id)
                result = '{"state":0}'
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result
