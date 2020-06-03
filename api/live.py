# coding=utf-8
import json
import random
import traceback
from urllib import unquote

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.http_utils import HttpUtils
from pycore.utils.logger_utils import LoggerUtils
from pycore.data.entity import globalvar as gl

from data.database import data_live_url, data_delete_room

logger = LoggerUtils('api.live').logger


def platform_reversed_cmp(x, y):
    if int(x["Number"]) < int(y["Number"]):
        return 1
    if int(x["Number"]) > int(y["Number"]):
        return -1
    return 0


def lives_reversed_cmp(x, y):
    if int(x["fire"]) < int(y["fire"]):
        return 1
    if int(x["fire"]) > int(y["fire"]):
        return -1
    return 0


def platform_list():
    result = '{"state":-1}'
    # connection = None
    try:
        # infile = open('./conf/live_platform.json')
        # result = '{"state":0, "data":%s}' % infile.read()
        # infile.close()
        connection = mysql_connection.get_conn()
        urls = data_live_url.query(connection)
        for url in urls:
            s1 = url.address.split("://")
            s2 = s1[1].index("/")
            js = HttpUtils(s1[1][0:s2]).get("/" + s1[1][s2 + 1:], None)
            platform_list_datas = json.loads(js)["pingtai"]
            for platform in platform_list_datas:
                platform["xinimg"] = platform["address"].replace("json", '').replace(".txt", ".jpg")
            platform_list_datas = sorted(platform_list_datas, cmp=platform_reversed_cmp)
            result = '{"state":0, "data":%s}' % json.dumps(platform_list_datas)
            break
    except:
        logger.exception(traceback.format_exc())
    # finally:
    #     if connection is not None:
    #         connection.close()
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
            delete_rooms = data_delete_room.delete_room_list(connection)
            live_datas = json.loads(js)["zhubo"]
            need_lives = []
            for live in live_datas:
                live["title"] = unquote(live["title"])
                if live["title"] not in delete_rooms:
                    if live["title"] in gl.get_v("fire"):
                        live["fire"] = gl.get_v("fire")[live["title"]]
                    else:
                        live["fire"] = random.randint(200, 500)
                    need_lives.append(live)
            need_lives = sorted(need_lives, cmp=lives_reversed_cmp)
            result = '{"state":0, "data":%s}' % (json.dumps(need_lives))
            break
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
