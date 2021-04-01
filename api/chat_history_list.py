import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_chat_history_list, data_chat_history
from utils import project_utils

logger = LoggerUtils('api.chat_history_list').logger


def query_list():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                page = int(data["page"])
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    chat_history_list = data_chat_history_list.query(connection, account_id, page)
                    message_count = data_chat_history.unread_count(connection, account_id)
                    result = '{"state":0, "data":[%s], "count":%d}' % (",".join(chat_history_list), message_count)
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def delete_list():
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
