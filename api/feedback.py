import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_feedback
from mode.feedback import Feedback
from utils import project_utils

logger = LoggerUtils('api.feedback').logger


def add():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            connection = None
            feedback = Feedback()
            if 0 == code:
                feedback.user_id = sessions["id"]
            if "HTTP_DEVICE" in request.headers.environ:
                feedback.device = request.headers.environ['HTTP_DEVICE']
            try:
                title = data["title"]
                content = data["content"]
                feedback.create_time = int(time.time())
                feedback.content = content
                feedback.title = title
                connection = mysql_connection.get_conn()
                data_feedback.create(connection, feedback)
                result = '{"state":0}'
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def query():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            account_id = 0
            device = ''
            if 0 == code:
                account_id = sessions["id"]
            if "HTTP_DEVICE" in request.headers.environ:
                device = request.headers.environ['HTTP_DEVICE']
            connection = None
            try:
                connection = mysql_connection.get_conn()
                page = int(data["page"])
                page_size = int(data["pageSize"])
                connection = mysql_connection.get_conn()
                feedback = data_feedback.query(connection, account_id, device, page, page_size)
                result = '{"state":0,"data":[%s]}' % (",".join(feedback))
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def info():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                connection = mysql_connection.get_conn()
                feedback_id = int(data["feedback_id"])
                connection = mysql_connection.get_conn()
                feedback = data_feedback.by_id(connection, feedback_id)
                result = '{"state":0,"data":%s}' % feedback
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result
