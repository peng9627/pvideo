# coding=utf-8
import json
import traceback

from pycore.data.entity import config, globalvar as gl

config.init("./conf/pyg.conf")
gl.init()
from pycore.data.database import mysql_connection
from pycore.utils import http_utils, time_utils

from data.database import data_movie
from mode.movie import Movie

if __name__ == '__main__':

    # page = 1
    # while True:
    #     s = http_utils.HttpUtils("taisinba.com").get_with_ssl(
    #         "/api/getcontents?page=%d&size=200&category=&type=movie,tv" % page, None)
    #     data = json.loads(s)
    #     if len(data) == 0:
    #         break
    #     else:
    #         out = open('./conf/movie_jsons/movie-%d.json' % page, 'w')
    #         out.write(json.dumps(data))
    #         out.close()
    #     page += 1 20.22.05

    for i in range(3, 102):

        infile = open('./conf/movie_jsons/movie-%d.json' % i, encoding="utf-8")
        videos = json.load(infile)
        infile.close()
        conn = None
        try:
            conn = mysql_connection.get_conn()
            for v in videos:
                movie = Movie()
                movie.type = 1
                movie.title = v["originalname"]
                movie.create_time = time_utils.string_to_stamp(v["createAt"], '%Y-%m-%dT%H:%M:%S.%fZ')
                movie.span = ",".join(v["tags"])
                movie.update_time = movie.create_time
                movie.actor = v["tags"][0]
                movie.horizontal = v["poster2"]["url"]
                movie.vertical = v["poster2"]["url"].replace("poster2.jpg", "poster730.jpg")
                # movie.vertical = v["poster2"]["url"].replace("poster2.jpg","poster350.jpg")
                movie.address = v["previewvideo"]
                s = http_utils.HttpUtils("taisinba.com").get_with_ssl("/api/getmovie?type=1280&id=" + v['_id'], None)
                url = json.loads(s)
                movie.address += "," + (url["m3u8"].split('?'))[0]
                data_movie.create(conn, movie)
        except:
            print(traceback.format_exc())
        finally:
            if conn is not None:
                conn.close()
