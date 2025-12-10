import json
import traceback
from pycore.data.entity import config, globalvar as gl

from utils.vtype import get_type_id

config.init("./conf/pyg.conf")
gl.init()
from pycore.data.database import mysql_connection

from data.database import data_movie
from mode.movie import Movie

if __name__ == '__main__':
    page = 9382
    pageCount = 9386
    while (page <= pageCount):
        videos = []
        with open('/Users/yi/project/old/project/pvideo/conf/vjs/v-' + str(page) + '.json', 'r') as f:
            videos = json.load(f)
        connection = mysql_connection.get_conn()
        try:
            for item in videos:
                video = Movie()
                video.type = get_type_id(item['type'])
                video.title = item['title']
                video.span = item['span']
                video.create_time = item['create_time']
                video.update_time = item['update_time']
                video.address = item['address']
                video.vertical = item['vertical']
                video.details = item['details']
                video.source = 'sw'
                data_movie.create(connection, video)
        except:
            print(page)
            print(traceback.format_exc())
        finally:
            connection.close()
        print("page" + str(page))
        page += 1
