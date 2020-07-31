import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_video_comment
from mode.video_comment import VideoComment

logger = LoggerUtils('api.video_comment').logger


def comment():
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
                video_comment = VideoComment()
                video_comment.user_id = account_id
                video_comment.video_id = video_id
                video_comment.create_time = int(time.time())
                video_comment.content = content
                data_video_comment.create_video_comment(connection, video_comment)
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
    connection = None
    data = request.form
    try:
        video_id = data["video_id"]
        page = int(data["page"])
        connection = mysql_connection.get_conn()
        comments = data_video_comment.query_comment(connection, video_id, page)
        comment_count = data_video_comment.video_comment_count(connection, video_id)
        result = '{"state":0,"data":[%s],"count":%d}' % (",".join(comments), comment_count)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
