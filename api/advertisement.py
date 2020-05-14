import re
import time
import traceback

from flask import request, session, make_response
from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl
from pycore.utils import http_utils
from pycore.utils.http_utils import HttpUtils
from pycore.utils.logger_utils import LoggerUtils
from pycore.utils.stringutils import StringUtils

from data.database import data_account, data_advertisement, data_advertisement_click
from mode.account import Account

logger = LoggerUtils('api.advertisement').logger


def query():
    result = '{"state":-1}'
    data = request.form
    where = data["where"]
    connection = None
    try:
        connection = mysql_connection.get_conn()
        advertisement = data_advertisement.query_advertisements(connection, where)
        result = '{"state":0, "data":[%s]}' % ",".join(advertisement)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def click():
    result = '{"state":-1}'
    data = request.form
    id = data["id"]
    connection = None
    account_id = 0
    try:
        connection = mysql_connection.get_conn()
        data_advertisement.add_count(connection, id)
        if "HTTP_AUTH" in request.headers.environ:
            sessionid = request.headers.environ['HTTP_AUTH']
            redis = gl.get_v("redis")
            if not redis.exists(sessionid):
                result = '{"state":2}'
            else:
                sessions = redis.getobj(sessionid)
                account_id = sessions["id"]
        data_advertisement_click.create_click(connection, id, account_id)
        result = '{"state":0}'
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
