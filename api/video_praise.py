import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_video_praise
from utils import project_utils

logger = LoggerUtils('api.video_praise').logger


def praise():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                video_id = data["video_id"]
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    data_video_praise.create_video_praise(connection, str(account_id) + ',' + video_id)
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


def cancel_praise():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                video_id = data["video_id"]
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    data_video_praise.cancel_video_praise(connection, str(account_id) + ',' + video_id)
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
#
# def is_praised():
#     result = '{"state":-1}'
#     data = request.form
#     if "HTTP_AUTH" in request.headers.environ:
#         sessionid = request.headers.environ['HTTP_AUTH']
#         redis = gl.get_v("redis")
#         if not redis.exists(sessionid):
#             result = '{"state":2}'
#         else:
#             sessions = redis.getobj(sessionid)
#             account_id = sessions["id"]
#             video_id = data["video_id"]
#             connection = None
#             try:
#                 connection = mysql_connection.get_conn()
#                 if data_video_praise.exist(connection, account_id + "," + video_id):
#
#                     result = '{"state":0,"data":1}'
#                 else:
#                     result = '{"state":0,"data":0}'
#             except:
#                 logger.exception(traceback.format_exc())
#             finally:
#                 if connection is not None:
#                     connection.close()
#     else:
#         result = '{"state":1}'
#     return result
