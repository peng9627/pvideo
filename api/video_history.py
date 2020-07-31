import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_video_history
from mode.video_history import VideoHistory

logger = LoggerUtils('api.video_history').logger


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
            video_id = data["video_id"]
            content = data["content"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                video_history = VideoHistory()
                video_history.user_id = account_id
                video_history.video_id = video_id
                video_history.video_type = 2
                video_history.update_time = int(time.time())
                video_history.content = content
                data_video_history.add_video_history(connection, video_history)
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
            result = '{"state":2}'
        else:
            sessions = redis.getobj(sessionid)
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                page = int(data["page"])
                connection = mysql_connection.get_conn()
                video_history = data_video_history.query_movie_history(connection, account_id, page)
                result = '{"state":0,"data":[%s]}' % (",".join(video_history))
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'
    return result
