import json
import traceback
import random
from urllib import unquote

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.http_utils import HttpUtils
from pycore.utils.logger_utils import LoggerUtils
from pycore.data.entity import globalvar as gl

from data.database import data_live_url, data_advertisement, data_video, data_vip_video, data_app_version, \
    data_delete_room

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


def index():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        urls = data_live_url.query(connection)
        js = ''
        advertisement1 = data_advertisement.query_advertisements(connection, 1)
        advertisement2 = data_advertisement.query_advertisements(connection, 2)
        vip_videos = data_vip_video.query(connection)
        if len(vip_videos) > 4:
            vip_videos = vip_videos[0:4]
        short_videos = data_video.query_video_list(connection, 21, 1, 6)
        videos = data_video.query_video_list(connection, -1, 1, 6)
        for url in urls:
            s1 = url.address.split("://")
            s2 = s1[1].index("/")
            js = HttpUtils(s1[1][0:s2]).get("/" + s1[1][s2 + 1:].replace("json.txt", "jsonxiaoxiannu.txt"), None)
            live_datas = json.loads(js)["zhubo"]
            delete_rooms = data_delete_room.delete_room_list(connection)
            need_lives = []
            for live in live_datas:
                live["title"] = unquote(live["title"])
                if live["title"] not in delete_rooms:
                    if live["title"] in gl.get_v("fire"):
                        live["fire"] = gl.get_v("fire")[live["title"]]
                    else:
                        live["fire"] = random.randint(200, 500)
                    need_lives.append(live)
            need_lives = sorted(need_lives, cmp=lives_reversed_cmp)[0:6]
            break
        result = '{"state":0, "lives":%s, "ads1":[%s], "ads2":[%s], "vip_videos":[%s], "short_videos":[%s], ' \
                 '"videos":[%s]}' % (json.dumps(need_lives), ",".join(advertisement1), ",".join(advertisement2), ",".join(vip_videos),
                                     ",".join(short_videos), ",".join(videos))
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
