import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl
from pycore.utils import http_utils, time_utils, aes_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_agent, data_account, data_gold
from utils import project_utils

logger = LoggerUtils('api.agent').logger


def first():
    result = '{"state":1}'
    try:
        ip = http_utils.get_client_ip(request.headers.environ)
        result = '{"state":0, "data":{"ip":"%s"}}' % ip
    except:
        logger.exception(traceback.format_exc())
    return result


def toip():
    result = '{"state":1}'
    data = request.form
    redis = gl.get_v("redis")
    try:
        code = data['code']
        ip = http_utils.get_client_ip(request.headers.environ)
        if ip is None or len(ip) < 1:
            ip = request.remote_addr
        if ip is not None and len(ip) > 1:
            redis.setex("ipinfo_" + ip, code, 86400)
            result = '{"state":0}'

    except:
        logger.exception(traceback.format_exc())
    return result


def my_agent_id():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        code, sessions = project_utils.get_auth(request.headers.environ)
        if 0 == code:
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                agent_id = data_agent.get_agent_id(connection, account_id)
                if agent_id is not None:
                    result = '{"state":0, "data":{"agent_id":"%s"}}' % agent_id
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        else:
            result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def users():
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
                page = int(data["page"])
                try:
                    connection = mysql_connection.get_conn()
                    users = data_account.by_parent(connection, account_id, page)
                    result = '{"state":0, "data":[%s]}' % ",".join(users)
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def join_agent():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                user_id = int(data["user_id"])
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    data_agent.join(connection, user_id, account_id)
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


def statistics():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        code, sessions = project_utils.get_auth(request.headers.environ)
        if 0 == code:
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                user_count = data_agent.user_count(connection, account_id)
                directly_count = data_agent.directly_count(connection, account_id)
                t = time.time()
                time_string = time_utils.stamp_to_string(t, '%Y/%m/%d')
                time_stamp = time_utils.string_to_stamp(time_string, '%Y/%m/%d') - 1
                today_new = data_agent.today_new(connection, account_id, time_stamp)
                today_active = data_agent.today_active(connection, account_id, time_stamp)
                give_gold = -data_gold.sum(connection, account_id, 5, 0)
                today_give_gold = -data_gold.sum(connection, account_id, 5, time_stamp)
                get_gold = data_gold.sum(connection, account_id, 6, 0)
                today_get_gold = data_gold.sum(connection, account_id, 6, time_stamp)
                result = '{"state":0, "data": {"user_count":%d, "directly_count":%d, "today_new":%d, ' \
                         '"today_active":%d, "give_gold":%d, "today_give_gold":%d, "get_gold":%d, ' \
                         '"today_get_gold":%d}} ' % (
                             user_count, directly_count, today_new, today_active, give_gold, today_give_gold,
                             get_gold, today_get_gold)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        else:
            result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result
