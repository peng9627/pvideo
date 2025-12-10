# coding=utf-8
import json
import time
import traceback

from pycore.data.entity import config, globalvar as gl
from pycore.utils import time_utils

from mode.movie import Movie

config.init("./conf/pyg.conf")
gl.init()

from data.database import data_movie
from pycore.data.database import mysql_connection

if __name__ == '__main__':
    page = 1
    connection = None
    try:
        connection = mysql_connection.get_conn()
        while page < 20:
            infile = open('./conf/movie_jsons/movie-%d.json' % page)
            videos = json.load(infile)
            infile.close()
            for v in videos["list"]:
                movie = Movie()
                movie.type = 1
                movie.title = v["vod_name"]
                movie.span = v["type_name"]
                movie.create_time = int(time.time())
                movie.update_time = time_utils.string_to_stamp(v["vod_time"], "%Y-%m-%d %H:%M:%S")
                movie.address = v["vod_play_url"]
                movie.horizontal = ''
                movie.vertical = v["vod_pic"]
                movie.actor = ''
                movie.child_type = v["type_name"]
                movie.director = ''
                movie.region = ''
                movie.year = ''
                movie.total_part = 1
                movie.details = v["vod_blurb"] + "\n\n" + v["vod_content"]
                movie.source = "sw"
                data_movie.create(connection, movie)
            page += 1
    except:
        print(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
