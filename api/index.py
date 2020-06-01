import json
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils.http_utils import HttpUtils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_live_url, data_advertisement, data_video, data_vip_video, data_app_version

logger = LoggerUtils('api.index').logger


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
            lives = json.loads(js)["zhubo"]
            if len(lives) > 6:
                lives = lives[0:6]
                js = json.dumps(lives)
            break
        result = '{"state":0, "lives":%s, "ads1":[%s], "ads2":[%s], "vip_videos":[%s], "short_videos":[%s], ' \
                 '"videos":[%s]}' % (js, ",".join(advertisement1), ",".join(advertisement2), ",".join(vip_videos),
                                     ",".join(short_videos), ",".join(videos))
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result
