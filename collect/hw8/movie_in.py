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
            infile = open('./conf/movie_jsons/hw8/movie-%d.json' % page)
            videos = json.load(infile)
            infile.close()
            for v in videos["list"]:
                movie = Movie()
                movie.type = v['type_id_1']
                movie.title = v["vod_name"]
                movie.span = v["vod_remarks"]
                movie.create_time = int(time.time())
                movie.update_time = time_utils.string_to_stamp(v["vod_time"], "%Y-%m-%d %H:%M:%S")
                movie.address = v["vod_play_url"]
                movie.horizontal = v["vod_pic"]
                movie.vertical = v["vod_pic"]
                movie.actor = v['vod_actor']
                type1 = v['type_id']
                tname = v['type_name']
                tsname = v['vod_class']
                if tname != tsname:
                    movie.child_type = tname + "," + tsname
                else:
                    movie.child_type = tname
                movie.director = v['vod_director']
                movie.region = v['vod_area']
                movie.year = v['vod_year']
                movie.total_part = v['vod_total']
                movie.details = v["vod_blurb"] + "\n\n" + v["vod_content"]
                movie.source = "hw8"
                data_movie.create(connection, movie)
            page += 1
    except:
        print(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
