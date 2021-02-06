import json
import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl
from pycore.utils import http_utils
from pycore.utils import time_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_agent, data_account, data_gold, data_vip
from mode.agent.agent import Agent
from mode.vip import Vip
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
                agent.create_time = int(time.time())
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

                directly_count = data_agent.agent_directly_count(connection, pagent.user_id)
                level_conf = json.loads(config.get("agent", "level_conf"))
                add_min = 0
                for lc in level_conf:
                    if directly_count >= lc["value"] and (add_min < lc["times"] or lc["times"] == -1):
                        add_min = lc["times"]
                    else:
                        break
                if pagent.min < add_min:
                    data_agent.add_min(connection, pagent.user_id, add_min - pagent.min)
                elif add_min == -1:
                    data_agent.add_min(connection, pagent.user_id, -1 - pagent.min)
                add_gold = int(config.get("server", "share_add_gold"))
                if 0 < add_gold:
                    data_account.update_gold(connection, add_gold, pagent.user_id)
                    data_gold.create_gold(connection, 2, 0, pagent.user_id, add_gold)
                share_add_vip_day = int(config.get("server", "share_add_vip_day"))
                if 0 < share_add_vip_day:
                    xj = data_agent.agent_directly_count(connection, pagent.user_id)
                    if 2 == xj:
                        share_add_vip_day = 5
                    elif xj > 2:
                        share_add_vip_day = 10
                    create_time = int(time.time())
                    last_end_time = data_vip.vip_end_time(connection, pagent.user_id)
                    if last_end_time > create_time:
                        start_time = last_end_time
                    else:
                        start_time = create_time
                    end_time = share_add_vip_day * 86400 + start_time
                    vip = Vip()
                    vip.account_id = pagent.user_id
                    vip.create_time = create_time
                    vip.start_time = start_time
                    vip.end_time = end_time
                    vip.order_no = ''
                    vip.operation_account = agent.user_id
                    data_vip.create_vip(connection, vip)
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
        ip = http_utils.get_client_ip(request.headers.environ)
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
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
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
        result = '{"state":%d}' % code
    return result


def my_contact():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
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
        result = '{"state":%d}' % code
    return result


def users():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        data = request.form
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
    return result


def join_agent():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        data = request.form
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
    return result


def agent_set():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        data = request.form
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
        result = '{"state":%d}' % code
    return result


def statistics():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        connection = None
        try:
            connection = mysql_connection.get_conn()
            user_count = data_agent.agent_user_count(connection, account_id)
            directly_count = data_agent.agent_directly_count(connection, account_id)
            t = time.time()
            time_string = time_utils.stamp_to_string(t, '%Y/%m/%d')
            time_stamp = time_utils.string_to_stamp(time_string, '%Y/%m/%d') - 1
            today_new = data_agent.agent_today_new(connection, account_id, time_stamp)
            today_active = data_agent.agent_today_active(connection, account_id, time_stamp)
            give_gold = -data_gold.gold_sum(connection, account_id, 5, 0)
            today_give_gold = -data_gold.gold_sum(connection, account_id, 5, time_stamp)
            get_gold = data_gold.gold_sum(connection, account_id, 6, 0)
            today_get_gold = data_gold.gold_sum(connection, account_id, 6, time_stamp)
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
    return result
