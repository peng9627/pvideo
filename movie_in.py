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
        while page < 138:
            infile = open('./conf/movie_jsons/movie-4-%d.json' % page)
            videos = json.load(infile)
            infile.close()
            for v in videos:
                movie = Movie()
                movie.type = 4
                movie.title = v["title"]
                movie.span = v["span"]
                movie.create_time = int(time.time())
                movie.update_time = time_utils.string_to_stamp(v["update_time"], "%Y-%m-%d %H:%M:%S")
                movie.address = v["address"]
                movie.horizontal = ''
                movie.vertical = v["vertical"]
                movie.actor = v["actor"]
                movie.child_type = v["child_type"]
                movie.director = v["director"]
                movie.region = v["region"]
                movie.year = v["year"]
                movie.total_part = 1
                movie.details = v["details"]
                movie.source = v["source"]
                data_movie.create(connection, movie)
            page += 1
    except:
        traceback.format_exc()
    finally:
        if connection is not None:
            connection.close()
