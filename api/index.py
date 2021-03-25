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
    data_notice, data_app_init, data_sign, data_account, data_gold
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
        app_version = data_app_version.query_app_version(connection, version_type, platform)
        result = '{"state":0,"data":%s}' % app_version
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def init_key():
    result = '{"state":-1}'
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
            result = '{"state":0,"key":"%s"}' % device_info['aes_key']
            connection = mysql_connection.get_conn()
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                t = time.time()
                time_string = time_utils.stamp_to_string(t, '%Y/%m/%d')
                time_stamp = time_utils.string_to_stamp(time_string, '%Y/%m/%d')
                # 今日没有签到
                if not data_sign.exist(connection, account_id, time_stamp):
                    # 昨天签到金币
                    last_gold = data_sign.sign_by_time(connection, account_id, time_stamp - 86400)
                    sign_golds = json.loads(config.get("server", "sign_golds"))
                    gold = 0
                    for g in sign_golds:
                        gold = g
                        if g > last_gold:
                            break
                    data_sign.sign(connection, account_id, time_stamp, gold)
                    data_account.update_gold(connection, gold, account_id)
                    data_gold.create_gold(connection, 3, 0, account_id, gold)
                    result = '{"state":0,"key":"%s","sign":%d}' % (device_info['aes_key'], gold)
            else:
                account_id = 0
            ip = http_utils.get_client_ip(request.headers.environ)
            data_app_init.app_init(connection, int(time.time()), account_id, device, ip)
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
