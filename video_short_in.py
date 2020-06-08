# coding=utf-8
import json
import os
import time

from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl

from utils.s3object import S3Object

config.init("./conf/pyg.conf")
gl.init()
from data.database import data_video
from mode.video import Video

if __name__ == '__main__':
    for i in range(21, 22):
        infile = open('/Users/pengyi/PycharmProjects/h5video/conf/short' + str(i) + '.json')
        videos = json.load(infile)
        infile.close()
        conn = None
        try:
            conn = mysql_connection.get_conn()
            for v in videos:
                filepath = v["filepath"]
                s3client = S3Object()
                logo_list = os.listdir("/home/video_tmp/" + filepath)
                # 2. which isn't file will be removed from logo_list
                for logo in logo_list:
                    if logo.endswith(".m3u8") or logo.endswith(".ts"):
                        s3client.upload("/home/video_tmp/" + filepath + "/" + logo, "dounai",
                                        "video/" + filepath + "/" + logo)

                video = Video()
                video.type = 0
                video.title = v["title"]
                video.create_time = int(time.time())
                video.address = "https://cdnt.dn1.live/video/" + filepath + "/" + filepath + ".m3u8"
                video.horizontal = ""
                video.vertical = ""
                connection = mysql_connection.get_conn()
                data_video.create_video(connection, video)
        except:
            print "error"
        finally:
            if conn is not None:
                conn.close()
