import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_video_comment
from mode.video_comment import VideoComment
from utils import project_utils

logger = LoggerUtils('api.video_comment').logger


def comment():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        data = request.form
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
        result = '{"state":%d}' % code
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
