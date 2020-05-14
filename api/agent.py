import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl
from pycore.utils import http_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_agent, data_account, data_gold
from mode.agent.agent import Agent

logger = LoggerUtils('api.agent').logger


def first():
    result = '{"state":1}'
    try:
        ip = http_utils.getClientIP(request.headers.environ)
        result = '{"state":0, "data":{"ip":"%s"}}' % ip
    except:
        logger.exception(traceback.format_exc())
    return result


def bind():
    result = '{"state":1}'
    connection = None
    data = request.form
    try:
        user_id = int(data['userid'])
        code = str(data['code'])
        ip = str(data['ip'])
        redis = gl.get_v("redis")
        connection = mysql_connection.get_conn()
        agent = data_agent.agent_by_id(connection, user_id)
        pid = None
        if agent is None:
            if code is not None and 1 < len(code):
                parent = data_account.query_account_by_code(connection, code)
                if parent is not None:
                    pid = parent.id
            if pid is None:
                if redis.exists("ipinfo_" + ip):
                    code = redis.get("ipinfo_" + ip)
                    parent = data_account.query_account_by_code(connection, code)
                    if parent is not None:
                        pid = parent.id
            if pid is None:
                pid = 10000
            pagent = data_agent.agent_by_id(connection, int(pid))
            if pagent is not None:
                agent = Agent()
                agent.user_id = user_id
                agent.parent_id = pagent.user_id
                if len(pagent.parent_ids) < 1:
                    agent.parent_ids = str(pagent.user_id)
                else:
                    agent.parent_ids = pagent.parent_ids + ',' + str(pagent.user_id)
                agent.top_id = pagent.top_id
                init_count = int(config.get("server", "init_min"))
                agent.commission = init_count
                agent.total_commission = init_count
                agent.contact = pagent.contact
                data_agent.add_agent(connection, agent)
                data_agent.add_min(connection, pagent.user_id)

                data_account.update_gold(connection, int(config.get("server", "share_add_gold")), pagent.user_id)
                data_gold.create_gold(connection, 2, 0, pagent.user_id, int(config.get("server", "share_add_gold")))
                result = '{"state":0}'

    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def toip():
    result = '{"state":1}'
    data = request.form
    redis = gl.get_v("redis")
    try:
        code = data['code']
        ip = http_utils.getClientIP(request.headers.environ)
        if ip is None or len(ip) < 1:
            ip = request.remote_addr
        if ip is not None and len(ip) > 1:
            redis.setex("ipinfo_" + ip, code, 86400)
            result = '{"state":0}'

    except:
        logger.exception(traceback.format_exc())
    return result


def agent_contact():
    result = '{"state":-1}'
    if "HTTP_AUTH" in request.headers.environ:
        sessionid = request.headers.environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        if not redis.exists(sessionid):
            result = '{"state":2}'
        else:
            sessions = redis.getobj(sessionid)
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                agent_id = data_agent.agent_get_parent_id(connection, account_id)
                contact = data_agent.agent_contact(connection, agent_id)
                result = '{"state":0, "data":{"contact":"%s"}}' % contact
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'
    return result


def my_contact():
    result = '{"state":-1}'
    if "HTTP_AUTH" in request.headers.environ:
        sessionid = request.headers.environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        if not redis.exists(sessionid):
            result = '{"state":2}'
        else:
            sessions = redis.getobj(sessionid)
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                contact = data_agent.agent_contact(connection, account_id)
                result = '{"state":0, "data":{"contact":"%s"}}' % contact
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'
    return result


def users():
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
        result = '{"state":1}'
    return result


def join_agent():
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
        result = '{"state":1}'
    return result


def agent_set():
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
            contact = data["contact"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                old_contact = data_agent.agent_contact(connection, account_id)
                data_agent.agent_set(connection, account_id, contact, old_contact)
                result = '{"state":0}'
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'
    return result
