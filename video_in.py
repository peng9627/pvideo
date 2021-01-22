# coding=utf-8
import json
import time
import traceback

from pycore.data.entity import config, globalvar as gl

config.init("./conf/pyg.conf")
gl.init()
from pycore.data.database import mysql_connection
from data.database import data_video
from mode.video import Video

if __name__ == '__main__':
    for i in range(3, 17):
        infile = open('/Users/pengyi/PycharmProjects/h5video/conf/hg' + str(i) + '.json')
        videos = json.load(infile)
        infile.close()
        conn = None
        try:
            conn = mysql_connection.get_conn()
            for v in videos["data"]:
                if "480P" in v["address"]:
                    video = Video()
                    video.type = i
                    video.title = v["movName"]
                    video.create_time = int(time.time())
                    video.address = v["address"]["480P"]
                    video.horizontal = v["allJCovers"]["horizontal_large"]
                    video.vertical = v["allJCovers"]["vertical_large"]
                    data_video.create_video(conn, video)
        except:
            print(traceback.format_exc())
        finally:
            if conn is not None:
                conn.close()
