# coding=utf-8
import json
import time

from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

config.init("./conf/pyg.conf")
gl.init()
from data.database import data_video
from mode.video import Video

if __name__ == '__main__':
    for i in range(21, 22):
        infile = open('/Users/pengyi/PycharmProjects/h5video/conf/hg' + str(i) + '.json')
        videos = json.load(infile)
        infile.close()
        conn = None
        try:
            conn = mysql_connection.get_conn()
            for v in videos["data"]:
                video = Video()
                video.type = i
                video.title = v["movName"]
                video.create_time = int(time.time())
                video.address = v["address"]["480P"]
                video.horizontal = v["allJCovers"]["horizontal_large"]
                video.vertical = v["allJCovers"]["vertical_large"]
                data_video.create_video(conn, video)
        except:
            print "error"
        finally:
            if conn is not None:
                conn.close()
