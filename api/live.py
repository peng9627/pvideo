import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.http_utils import HttpUtils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_vip_video, data_live_url

logger = LoggerUtils('api.live').logger


def platform_list():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        urls = data_live_url.query(connection)
        for url in urls:
            s1 = url.address.split("://")
            s2 = s1[1].index("/")
            js = HttpUtils(s1[1][0:s2]).get("/" + s1[1][s2 + 1:], None)
            result = '{"state":0, "data":%s}' % js
            break
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def lives():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        address = data["address"]
        connection = mysql_connection.get_conn()
        urls = data_live_url.query(connection)
        for url in urls:
            s1 = url.address.split("://")
            s2 = s1[1].index("/")
            js = HttpUtils(s1[1][0:s2]).get("/" + s1[1][s2 + 1:].replace("json.txt", address), None)
            result = '{"state":0, "data":%s}' % js
            break
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
