import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_feedback
from mode.feedback import Feedback

logger = LoggerUtils('api.feedback').logger


def add():
    result = '{"state":-1}'
    data = request.form
    if "HTTP_AUTH" in request.headers.environ:
        sessionid = request.headers.environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        if not redis.exists(sessionid):
            result = '{"state":2}'
        else:
            sessions = redis.getobj(sessionid)
            account_id = sessions["id"]
            title = data["title"]
            content = data["content"]

            feedback = Feedback()
            feedback.user_id = account_id
            feedback.create_time = int(time.time())
            feedback.content = content
            feedback.title = title
            connection = None
            try:
                connection = mysql_connection.get_conn()
                data_feedback.add_feedback(connection, feedback)
                result = '{"state":0}'
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'

    return result


def query():
    result = '{"state":-1}'
    data = request.form
    if "HTTP_AUTH" in request.headers.environ:
        sessionid = request.headers.environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        if not redis.exists(sessionid):
            return '{"state":2}'
        else:
            sessions = redis.getobj(sessionid)
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                page = int(data["page"])
                connection = mysql_connection.get_conn()
                feedback = data_feedback.query(connection, account_id, page)
                result = '{"state":0,"data":[%s]}' % (",".join(feedback))
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        return '{"state":1}'
    return result


def info():
    result = '{"state":-1}'
    data = request.form
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
    return result
