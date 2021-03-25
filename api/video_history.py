import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_video_history
from mode.video_history import VideoHistory
from utils import project_utils

logger = LoggerUtils('api.video_history').logger


def add():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                video_history = VideoHistory()
                video_history.user_id = account_id
                if "HTTP_DEVICE" in request.headers.environ:
                    device = request.headers.environ['HTTP_DEVICE']
                    video_history.device = device
                video_id = data["video_id"]
                content = data["content"]
                connection = None
                try:
                    connection = mysql_connection.get_conn()
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
                result = '{"state":%d}' % code
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
            if 0 == code:
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
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result
