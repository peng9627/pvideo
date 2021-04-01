import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_chat_history_list, data_chat_history
from utils import project_utils

logger = LoggerUtils('api.chat_history').logger


def list():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                uid = data["uid"]
                create_time = data["create_time"]
                if 0 == create_time:
                    create_time = int(time.time()) + 2
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    chat_history = data_chat_history.query(connection, account_id, uid, create_time)
                    result = '{"state":0, "data":[%s]}' % ",".join(chat_history)
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def delete():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                to_id = int(data["to_id"])
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    data_chat_history_list.delete(connection, account_id, to_id)
                    result = '{"state":0}'
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def receive():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                to_id = int(data["to_id"])
                create_time = int(data["time"])
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    data_chat_history.receive(connection, int(time.time()), create_time, to_id, account_id)
                    data_chat_history_list.receive(connection, account_id, to_id)
                    result = '{"state":0}'
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result
