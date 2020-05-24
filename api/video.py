import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_video_type, data_video

logger = LoggerUtils('api.video').logger


def query_type():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        types = data_video_type.query_types(connection)
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
        videos = data_video.query_video_list(connection, type, page)
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
        videos = data_video.query_video_search(connection, content, page)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
