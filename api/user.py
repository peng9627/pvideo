# coding=utf-8
import re
import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl, config
from pycore.utils import http_utils
from pycore.utils.http_utils import HttpUtils
from pycore.utils.logger_utils import LoggerUtils
from pycore.utils.stringutils import StringUtils

from data.database import data_account, data_agent, data_vip, data_gold
from mode.account import Account

logger = LoggerUtils('api.user').logger


def login_success(redis, account):
    sessionid = 'session' + StringUtils.randomStr(32)
    while redis.exists(sessionid):
        sessionid = 'session' + StringUtils.randomStr(32)
    sessions = {'id': account.id}
    redis.setexo(sessionid, sessions, 604800)
    return sessionid


def login():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        connection = mysql_connection.get_conn()
        account_name = str(data['account'])
        pwd = str(data['pwd'])
        account = data_account.query_account_by_account_name(connection, account_name)
        if account is None:
            result = '{"state":1}'
        elif StringUtils.md5(pwd + account.salt) != account.pwd:
            result = '{"state":2}'
        elif account.account_status != 0:
            result = '{"state":3}'
        else:
            data_account.update_login(time.time(), connection, http_utils.getClientIP(request.headers.environ),
                                      account.id)
            result = '{"state":0,"auth":"' + login_success(gl.get_v("redis"), account) + '"}'
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def register():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        connection = mysql_connection.get_conn()
        account_name = str(data['account'])
        pwd = str(data['pwd'])
        username = re.compile(r"[0-9a-zA-Z_]{8,16}")
        if username.match(account_name):
            code = str(data['code'])
            if not gl.get_v("redis").exists(account_name + '_code'):
                result = '{"state":1}'
            elif code != gl.get_v("redis").get(account_name + '_code'):
                result = '{"state":2}'
            elif data_account.exist(connection, account_name):
                result = '{"state":3}'
            else:
                share_code = ''
                if "share_code" in data:
                    share_code = str(data['share_code'])
                share_ip = ''
                if "share_ip" in data:
                    share_ip = str(data['share_ip'])
                account = Account()
                account.account_name = account_name
                account.nickname = "zz" + account_name[-4:]
                account.create_time = int(time.time())
                account.salt = StringUtils.randomStr(32)
                account.pwd = StringUtils.md5(pwd + account.salt)
                account.code = StringUtils.randomStr(4).upper()
                while data_account.exist_code(connection, account.code):
                    account.code = StringUtils.randomStr(4).upper()
                last_address = http_utils.getClientIP(request.headers.environ)
                data_account.create_account(connection, account, last_address, share_code, share_ip)
                result = '{"state":0}'
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def change_pwd():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        connection = mysql_connection.get_conn()
        account_name = str(data['account'])
        pwd = str(data['pwd'])
        username = re.compile(r"[0-9a-zA-Z_]{8,16}")
        if username.match(account_name):
            code = str(data['code'])
            if not gl.get_v("redis").exists(account_name + '_code'):
                result = '{"state":1}'
            elif code != gl.get_v("redis").get(account_name + '_code'):
                result = '{"state":2}'
            else:
                account = data_account.query_account_by_account_name(connection, account_name)
                if account is None:
                    result = '{"state":3}'
                else:
                    pwd = StringUtils.md5(pwd + account.salt)
                    data_account.update_pwd(connection, pwd, account.id)
                    result = '{"state":0}'
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def send_code():
    result = '{"state":-1}'
    data = request.form
    account_name = str(data['account'])
    try:
        if not re.match(r"^1[3456789]\d{9}$", account_name):
            result = '{"state":1}'
        elif gl.get_v("redis").exists(account_name + '_code'):
            result = '{"state":2}'
        else:
            code = StringUtils.randomNum(6)
            enc = StringUtils.md5(
                config.get("sms", "sms_user") + StringUtils.md5(config.get("sms", "sms_key")))
            content = "【至尊娱乐】验证码：" + code + "，请在3分钟内正确输入。"
            msg = HttpUtils("sms-cly.cn").get("/smsSend.do?username=" + config.get("sms",
                                                                                   "sms_user") + "&password=" + enc + "&mobile=" + account_name + "&content=" + content,
                                              None)
            gl.get_v("redis").setex(account_name + "_code", code, 120)
            logger.info(code)
            result = '{"state":0}'
    except:
        logger.exception(traceback.format_exc())
    return result


def info():
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
                account = data_account.query_account_by_id(connection, account_id)
                if account is not None:
                    agent = data_agent.agent_by_id(connection, account.id)
                    end_time = data_vip.vip_end_time(connection, account.id)
                    if 0 == end_time:
                        vip = u"普通会员"
                    elif end_time < time.time():
                        vip = u"VIP会员已过期"
                    else:
                        this_time = int(time.time())
                        if end_time - this_time > 86400:
                            vip = u"VIP会员有效期:" + str((end_time - this_time) / 86400) + u"天"
                        elif end_time - this_time > 3600:
                            vip = u"VIP会员有效期:" + str((end_time - this_time) / 3600) + u"小时"
                        else:
                            vip = u"VIP会员有效期:" + str((end_time - this_time) / 60) + u"分钟"
                    result = '{"state":0, "data":{"id":%d, "head":"%s", "nickname":"%s", "sex":%d, "gold":%d, ' \
                             '"min":%d, "total_min":%d, "status":%d, "vip":"%s", "code":"%s"}}' % (
                                 account_id, "" if account.head is None else account.head, account.nickname,
                                 account.sex, account.gold, agent.min, agent.total_min, agent.status, vip, account.code)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'
    return result


def give_gold():
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
            give_gold = int(data["give_gold"])
            if give_gold > 0:
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    parent_id = data_agent.agent_get_parent_id(connection, user_id)
                    if parent_id != int(account_id):
                        result = '{"state":3}'
                    else:
                        account = data_account.query_account_by_id(connection, account_id)
                        if account.gold < give_gold:
                            result = '{"state":4}'
                        else:
                            data_account.update_gold(connection, -give_gold, account_id)
                            data_gold.create_gold(connection, 5, 0, account_id, -give_gold)

                            data_account.update_gold(connection, give_gold, user_id)
                            data_gold.create_gold(connection, 6, 0, user_id, give_gold)
                            result = '{"state":0}'
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
    else:
        result = '{"state":1}'
    return result


def check_time():
    result = '{"state":-1}'
    data = request.form
    use_time = int(data["time"])
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
                if data_vip.is_vip(connection, account_id):
                    surplus_time = 100000
                else:
                    if use_time > 0:
                        data_agent.use_min(connection, account_id, use_time)
                    surplus_time = data_agent.query_min(connection, account_id)
                    if surplus_time < 0:
                        data_agent.use_min(connection, account_id, -surplus_time)
                        surplus_time = 0
                result = '{"state":0,"data":{"surplus_time":%d}}' % surplus_time
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
    else:
        result = '{"state":1}'
    return result
