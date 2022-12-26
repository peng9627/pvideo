# coding=utf-8
import json
import math
import re
import smtplib
import time
import traceback
from email.header import Header
from email.mime.text import MIMEText

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl, config
from pycore.utils import http_utils, aes_utils
from pycore.utils.http_utils import HttpUtils
from pycore.utils.logger_utils import LoggerUtils
from pycore.utils.stringutils import StringUtils

from data.database import data_account, data_agent, data_vip, data_gold
from mode.account import Account
from mode.agent import Agent
from mode.vip import Vip
from utils import project_utils

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
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                connection = mysql_connection.get_conn()
                account_name = str(data['account'])
                pwd = str(data['pwd'])
                account = data_account.query_by_account_name(connection, account_name)
                if account is None:
                    result = '{"state":1}'
                elif StringUtils.md5(pwd + account.salt) != account.pwd:
                    result = '{"state":2}'
                elif account.account_status != 0:
                    result = '{"state":3}'
                else:
                    data_account.update_login(time.time(), connection,
                                              http_utils.get_client_ip(request.headers.environ),
                                              account.id)
                    return aes_utils.aes_encode('{"state":0}', key), 200, {
                        'auth': login_success(gl.get_v("redis"), account)}
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def register():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                connection = mysql_connection.get_conn()
                account_name = str(data['account'])
                pwd = str(data['pwd'])
                # if re.match(r"^1[3456789]\d{9}$", account_name and re.match(r"[0-9a-zA-Z_]{8,16}", pwd):
                if 5 < len(account_name) < 13 and re.match(r"[0-9a-zA-Z_]{5,16}", pwd):
                    if data_account.exist(connection, account_name):
                        result = '{"state":3}'
                    elif "HTTP_DEVICE" in request.headers.environ:
                        device = request.headers.environ['HTTP_DEVICE']
                        device_count = data_account.device_count(connection, device)
                        if device_count >= int(config.get("server", "same_device_register")):
                            result = '{"state":4}'
                        else:
                            account = Account()
                            account.account_name = account_name
                            account.nickname = "dm" + StringUtils.randomStr(6)
                            account.create_time = int(time.time())
                            account.salt = StringUtils.randomStr(32)
                            account.pwd = StringUtils.md5(pwd + account.salt)
                            account.code = StringUtils.randomStr(4).upper()
                            account.device = device
                            while data_account.exist_code(connection, account.code):
                                account.code = StringUtils.randomStr(4).upper()
                            last_address = http_utils.get_client_ip(request.headers.environ)
                            data_account.create(connection, account, last_address)
                            account = data_account.query_by_account_name(connection, account.account_name)
                            if account is not None:
                                data_account.update_gold(connection, int(config.get("server", "register_gold")),
                                                         account.id)
                                data_gold.create(connection, 1, 0, account.id,
                                                 int(config.get("server", "register_gold")))

                                agent = data_agent.by_id(connection, account.id)
                                pid = None
                                if agent is None:
                                    share_code = ''
                                    if "code" in data:
                                        share_code = str(data['code'])
                                    # 通过推广码找代理
                                    if share_code is not None and 1 < len(share_code):
                                        parent = data_account.query_id_by_code(connection, share_code)
                                        if parent is not None:
                                            pid = parent
                                    # 通过ip找代理
                                    if pid is None and "share_code" in data:
                                        share_code = str(data['share_code'])
                                    # 通过推广码找代理
                                    if share_code is not None and 1 < len(share_code):
                                        parent = data_account.query_id_by_code(connection, share_code)
                                        if parent is not None:
                                            pid = parent
                                    # 通过ip找代理
                                    if pid is None and "share_ip" in data:
                                        share_ip = str(data['share_ip'])
                                        redis = gl.get_v("redis")
                                        if redis.exists("ipinfo_" + share_ip):
                                            share_code = redis.get("ipinfo_" + share_ip)
                                            parent = data_account.query_id_by_code(connection, share_code)
                                            if parent is not None:
                                                pid = parent
                                    pagent = None
                                    # 没代理自动绑定平台
                                    if pid is not None:
                                        pagent = data_agent.by_id(connection, int(pid))
                                    agent = Agent()
                                    agent.create_time = int(time.time())
                                    agent.user_id = account.id
                                    init_count = int(config.get("server", "init_times"))
                                    agent.commission = init_count
                                    agent.total_commission = init_count
                                    agent.top_id = account.id
                                    create_time = int(time.time())
                                    if pagent is not None:
                                        agent.parent_id = pagent.user_id
                                        if len(pagent.parent_ids) < 1:
                                            agent.parent_ids = str(pagent.user_id)
                                        else:
                                            agent.parent_ids = pagent.parent_ids + ',' + str(pagent.user_id)
                                        agent.top_id = pagent.top_id
                                        agent.contact = pagent.contact
                                        directly_count = data_agent.directly_count(connection, pagent.user_id)
                                        # vip等级
                                        level_conf = json.loads(config.get("agent", "level_conf"))
                                        add_times = 0
                                        for lc in level_conf:
                                            if directly_count >= lc["value"] and (
                                                    add_times < lc["times"] or lc["times"] == -1):
                                                add_times = lc["times"]
                                            else:
                                                break
                                        if pagent.times < add_times:
                                            data_agent.add_times(connection, pagent.user_id,
                                                                 add_times - pagent.total_times,
                                                                 add_times - pagent.total_times)
                                        elif add_times == -1:
                                            data_agent.add_times(connection, pagent.user_id, -1 - pagent.times,
                                                                 -1 - pagent.total_times)
                                        add_gold = int(config.get("server", "share_add_gold"))
                                        if 0 < add_gold:
                                            data_account.update_gold(connection, add_gold, pagent.user_id)
                                            data_gold.create(connection, 2, 0, pagent.user_id, add_gold)
                                        # 推广送vip天数 双向
                                        share_add_vip_day = int(config.get("server", "share_add_vip_day"))
                                        if 0 < share_add_vip_day:
                                            last_end_time = data_vip.end_time(connection, pagent.user_id)
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
                                            vip.operation_account = account.id
                                            data_vip.create(connection, vip)

                                            # # 注册送vip天数
                                            # last_end_time = data_vip.end_time(connection, account.id)
                                            # if last_end_time > create_time:
                                            #     start_time = last_end_time
                                            # else:
                                            #     start_time = create_time
                                            # end_time = share_add_vip_day * 86400 + start_time
                                            # vip = Vip()
                                            # vip.account_id = account.id
                                            # vip.create_time = create_time
                                            # vip.start_time = start_time
                                            # vip.end_time = end_time
                                            # vip.order_no = ''
                                            # vip.operation_account = account.id
                                            # data_vip.create(connection, vip)
                                            # 注册送vip天数
                                            register_vip_day = int(config.get("server", "register_vip_day"))
                                            if 0 < register_vip_day:
                                                last_end_time = data_vip.end_time(connection, account.id)
                                                if last_end_time > create_time:
                                                    start_time = last_end_time
                                                else:
                                                    start_time = create_time
                                                end_time = register_vip_day * 86400 + start_time
                                                vip = Vip()
                                                vip.account_id = account.id
                                                vip.create_time = create_time
                                                vip.start_time = start_time
                                                vip.end_time = end_time
                                                vip.order_no = ''
                                                vip.operation_account = account.id
                                                data_vip.create(connection, vip)
                                    data_agent.create(connection, agent)
                            result = '{"state":0}'
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def change_pwd():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                connection = mysql_connection.get_conn()
                account_name = str(data['account'])
                pwd = str(data['pwd'])
                old_pwd = str(data['old_pwd'])
                if 5 < len(account_name) < 13 and re.match(r"[0-9a-zA-Z_]{5,16}", pwd) and re.match(
                        r"[0-9a-zA-Z_]{5,16}", old_pwd):
                    account = data_account.query_by_account_name(connection, account_name)
                    if account is None:
                        result = '{"state":3}'
                    elif StringUtils.md5(old_pwd + account.salt) != account.pwd:
                        result = '{"state":4}'
                    else:
                        pwd = StringUtils.md5(pwd + account.salt)
                        data_account.update_pwd(connection, pwd, account.id)
                        result = '{"state":0}'
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def send_code():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            account_name = str(data['account'])
            # if re.match(r"^1[3456789]\d{9}$", account_name):
            if re.match(r"^1[3456789]\d{9}$", account_name) or re.match(
                    r"^[A-Za-z0-9]+([_.][A-Za-z0-9]+)*@([A-Za-z0-9-]+.)+[A-Za-z]{2,6}$", account_name):
                try:
                    if gl.get_v("redis").exists(account_name + '_code'):
                        result = '{"state":2}'
                    else:
                        code = StringUtils.randomNum(6)
                        if re.match(r"^1[3456789]\d{9}$", account_name):
                            enc = StringUtils.md5(
                                config.get("sms", "sms_user") + StringUtils.md5(config.get("sms", "sms_key")))
                            content = "【至尊娱乐】验证码：" + code + "，请在3分钟内正确输入。"
                            msg = HttpUtils("sms-cly.cn").get("/smsSend.do?username=" + config.get("sms",
                                                                                                   "sms_user") + "&password=" + enc + "&mobile=" + account_name + "&content=" + content,
                                                              None)
                        else:
                            mail_sender = config.get("mail", "mail_sender")  # 发件人邮箱账号
                            mail_pass = config.get("mail", "mail_pass")  # 发件人邮箱密码
                            receivers = account_name  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

                            # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
                            message = MIMEText('【哒咪】验证码：' + code, 'plain', 'utf-8')
                            message['From'] = Header("dm", 'utf-8')

                            subject = 'dm code'
                            message['Subject'] = Header(subject, 'utf-8')

                            server = smtplib.SMTP(config.get("mail", "mail_host"),
                                                  int(config.get("mail", "mail_port")))  # 发件人邮箱中的SMTP服务器，端口是25
                            server.ehlo()  # 向邮箱发送SMTP 'ehlo' 命令
                            server.starttls()
                            server.login(mail_sender, mail_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                            server.sendmail(mail_sender, [receivers], message.as_string())
                        gl.get_v("redis").setex(account_name + "_code", code, 120)
                        logger.info(code)
                        result = '{"state":0}'
                except:
                    logger.exception(traceback.format_exc())
        return aes_utils.aes_encode(result, key)
    return result


def info():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        code, sessions = project_utils.get_auth(request.headers.environ)
        if 0 == code:
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                account = data_account.query_by_id(connection, account_id)
                if account is not None:
                    agent = data_agent.by_id(connection, account.id)
                    end_time = data_vip.end_time(connection, account.id)
                    if 0 == end_time:
                        vip = u"VIP会员"
                    elif end_time < time.time():
                        vip = u"SVIP会员已过期"
                    else:
                        this_time = int(time.time())
                        if end_time - this_time > 86400:
                            vip = u"SVIP会员有效期:%.0f天" % math.ceil((end_time - this_time) / 86400.0)
                        elif end_time - this_time > 3600:
                            vip = u"SVIP会员有效期:%.0f小时" % math.ceil((end_time - this_time) / 3600.0)
                        else:
                            vip = u"SVIP会员有效期:%.0f分钟" % math.ceil((end_time - this_time) / 60.0)
                    directly_count = data_agent.directly_count(connection, account.id)
                    level_conf = json.loads(config.get("agent", "level_conf"))
                    add_times = 0
                    level = 1
                    next = 0
                    for lc in level_conf:
                        if directly_count >= lc["value"] and (add_times < lc["times"] or lc["times"] == -1):
                            add_times = lc["times"]
                            level = lc["level"]
                            next = lc["value"]
                        else:
                            next = lc["value"] - next
                            break
                    result = '{"state":0, "data":{"id":%d, "head":"%s", "nickname":"%s", "sex":%d, "gold":%d, ' \
                             '"times":%d, "total_times":%d, "status":%d, "vip":"%s", "level":%d, "next":%d, "code":"%s"}}' % (
                                 account_id, "" if account.head is None else account.head, account.nickname,
                                 account.sex, account.gold, agent.times, agent.total_times, agent.status, vip, level,
                                 next, account.code)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        else:
            result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def get_name():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                user_id = int(data["user_id"])
                connection = None
                try:
                    connection = mysql_connection.get_conn()
                    account = data_account.query_by_id(connection, user_id)
                    if account is not None:
                        result = '{"state":0,"data":"%s"}' % account.nickname
                except:
                    logger.exception(traceback.format_exc())
                finally:
                    if connection is not None:
                        connection.close()
            else:
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result


def give_gold():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                data = request.form
                user_id = int(data["user_id"])
                give_gold = int(data["give_gold"])
                if give_gold > 0:
                    connection = None
                    try:
                        connection = mysql_connection.get_conn()
                        parent_id = data_agent.get_parent_id(connection, user_id)
                        if parent_id != int(account_id):
                            result = '{"state":3}'
                        else:
                            account = data_account.query_by_id(connection, account_id)
                            if account.gold < give_gold:
                                result = '{"state":4}'
                            else:
                                data_account.update_gold(connection, -give_gold, account_id)
                                data_gold.create(connection, 5, 0, account_id, -give_gold)

                                data_account.update_gold(connection, give_gold, user_id)
                                data_gold.create(connection, 6, 0, user_id, give_gold)
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


def check_time():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        code, sessions = project_utils.get_auth(request.headers.environ)
        if 0 == code:
            account_id = sessions["id"]
            connection = None
            try:
                connection = mysql_connection.get_conn()
                if data_vip.is_vip(connection, account_id):
                    surplus_time = -1
                else:
                    surplus_time = data_agent.query_times(connection, account_id)
                    if surplus_time < 0:
                        surplus_time = 0
                result = '{"state":0,"data":{"surplus_time":%d}}' % surplus_time
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        elif 1 == code:
            if "HTTP_DEVICE" in request.headers.environ:
                device = request.headers.environ['HTTP_DEVICE']
                redis = gl.get_v("redis")
                if redis.exists("device_info_" + device):
                    device_info = redis.getobj("device_info_" + device)
                    surplus_time = device_info['surplus_time']
                else:
                    surplus_time = int(config.get("server", "default_times"))
                result = '{"state":0,"data":{"surplus_time":%d, "total_time":%s}}' % (
                    surplus_time, config.get("server", "default_times"))
            else:
                result = '{"state":1}'
        else:
            result = '{"state":2}'
        return aes_utils.aes_encode(result, key)
    return result
