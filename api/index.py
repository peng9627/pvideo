import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl
from pycore.utils.logger_utils import LoggerUtils
from pycore.utils.stringutils import StringUtils

from data.database import data_advertisement, data_app_version, \
    data_notice
from utils import project_utils, aes_utils

logger = LoggerUtils('api.index').logger


def lives_reversed_cmp(x, y):
    if int(x["fire"]) < int(y["fire"]):
        return 1
    if int(x["fire"]) > int(y["fire"]):
        return -1
    return 0


def version():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        connection = mysql_connection.get_conn()
        platform = data["platform"]
        version_type = data["type"]
        app_version = data_app_version.query_app_version(connection, version_type, platform)
        result = '{"state":0,"data":%s}' % app_version
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


# def init_key():
#     times = time.time()
#     result = '{"state":-1}'
#     try:
#         if "HTTP_DEVICE" in request.headers.environ:
#             device = request.headers.environ['HTTP_DEVICE']
#             redis = gl.get_v("redis")
#             if redis.exists("device_info_" + device):
#                 device_info = redis.getobj("device_info_" + device)
#             else:
#                 device_info = {'surplus_time': int(config.get("server", "default_min"))}
#             print(time.time() - times)
#             server_pub, server_pri = rsa_utils.new_keys(2048)
#             client_pub, client_pri = rsa_utils.new_keys(2048)
#             print(time.time() - times)
#             device_info['pri'] = server_pri
#             device_info['pub'] = client_pub
#             redis.setexo("device_info_" + device, device_info, 18000)
#             result = '{"state":0,"pri":"%s","pub":"%s"}' % (client_pri.replace('\n','\\n'), server_pub.replace('\n','\\n'))
#         else:
#             result = '{"state":1}'
#     except:
#         logger.exception(traceback.format_exc())
#     print(time.time() - times)
#     return result


def init_key():
    result = '{"state":-1}'
    try:
        if "HTTP_DEVICE" in request.headers.environ:
            device = request.headers.environ['HTTP_DEVICE']
            redis = gl.get_v("redis")
            if redis.exists("device_info_" + device):
                device_info = redis.getobj("device_info_" + device)
            else:
                device_info = {'surplus_time': int(config.get("server", "default_min"))}
            device_info['aes_key'] = StringUtils.randomStr(16)
            redis.setexo("device_info_" + device, device_info, 18000)
            result = '{"state":0,"key":"%s"}' % device_info['aes_key']
        else:
            result = '{"state":1}'
    except:
        logger.exception(traceback.format_exc())
    return result


def index():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        connection = None
        try:
            connection = mysql_connection.get_conn()
            advertisement1 = data_advertisement.query_advertisements(connection, 1)
            advertisement2 = data_advertisement.query_advertisements(connection, 2)
            notice_s = ''
            notice = data_notice.query(connection, 1)
            if notice is not None:
                notice_s = notice.content
            result = '{"state":0, "notice":"%s", "ads1":[%s], "ads2":[%s]}' % (
                notice_s, ",".join(advertisement1), ",".join(advertisement2))
        except:
            logger.exception(traceback.format_exc())
        finally:
            if connection is not None:
                connection.close()
        return aes_utils.aes_encode(result, key)
    return result
