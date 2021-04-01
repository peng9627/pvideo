import json
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_video_type, data_video, data_video_praise, data_video_comment
from utils import project_utils

logger = LoggerUtils('api.video').logger


def query_type():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        types = data_video_type.query(connection)
        result = '{"state":0, "data":[%s]}' % ",".join(types)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def query_video():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        type = int(data["type"])
        page = int(data["page"])
        connection = mysql_connection.get_conn()
        videos = data_video.list(connection, type, page)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def recommend():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        videos = data_video.recommend(connection)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def search():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        content = data["content"]
        page = int(data["page"])
        connection = mysql_connection.get_conn()
        videos = data_video.search(connection, content, page)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def query_details():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        video_id = data["video_id"]
        connection = mysql_connection.get_conn()
        praises = data_video_praise.count(connection, '%,' + str(video_id))
        comments = data_video_comment.count(connection, video_id)
        praised = False
        code, sessions = project_utils.get_auth(request.headers.environ)
        if 0 == code:
            account_id = sessions["id"]
            praised = data_video_praise.exist(connection, str(account_id) + "," + video_id)
        result = '{"state":0, "data":{"praises":%d, "comments":%d, "praised":%d}}' % (
            praises, comments, 1 if praised else 0)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def query_info():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        video_id = data["video_id"]
        connection = mysql_connection.get_conn()
        video_data = data_video.info(connection, video_id)
        video_data["praises"] = data_video_praise.count(connection, '%,' + str(video_id))
        praised = False
        code, sessions = project_utils.get_auth(request.headers.environ)
        if 0 == code:
            account_id = sessions["id"]
            praised = data_video_praise.exist(connection, str(account_id) + "," + video_id)
        video_data["praised"] = 1 if praised else 0
        result = '{"state":0, "data":%s}' % json.dumps(video_data)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
