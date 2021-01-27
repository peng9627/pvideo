# coding=utf-8
import json
import time
import traceback

import requests
from pycore.data.entity import config, globalvar as gl

config.init("./conf/pyg.conf")
gl.init()

from pycore.data.database import mysql_connection

from data.database import data_movie
from mode.movie import Movie

if __name__ == '__main__':
    channel_id = 50  # 1.3 2.2 3.50 4.1
    url = 'https://pianku.api.mgtv.com/rider/list/pcweb/v3?platform=pcweb&channelId=%d&pn=%d&pc=80&hudong=1&_support=10000000&kind=a1&area=a1&year=all&sort=c2&edition=all&chargeInfo=a1'
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9',
        'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    }
    header_pc = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
    }
    for i in range(1, 2):
        url1 = url % (channel_id, i)
        response = requests.get(url1, headers=header_pc)
        response.encoding = 'utf-8'
        videos = response.json()['data']['hitDocs']
        for v in videos:
            connection = None
            try:
                img = v['img']
                name = v['title']
                year = v['year']
                desc = v['story']
                videoDetails1 = requests.get('https://pcweb.api.mgtv.com/video/info?vid=%s&cid=%s&_support=10000000' % (
                    v['playPartId'], v['clipId']), headers=header)
                videoDetails1.encoding = 'utf-8'
                videoDetails1 = videoDetails1.json()['data']['info']['detail']
                span = videoDetails1['updateInfo']
                region = videoDetails1['area']
                mainActors = videoDetails1['leader'].lstrip().replace('/', ',')
                tags = videoDetails1['kind'].lstrip().replace('/', ',')
                directors = videoDetails1['director'].lstrip().replace('/', ',')
                createTime = int(time.time())
                updateTime = int(time.time())
                videoCount = 0
                if 3 != channel_id:
                    address = ''
                    page = 0
                    totalPage = 1
                    while page < totalPage:
                        page += 1
                        parts = requests.get(
                            'https://pcweb.api.mgtv.com/episode/list?_support=10000000&version=5.5.35&video_id=%s&page=%d&size=30' % (
                                v['playPartId'], page), headers=header_pc)
                        parts.encoding = 'utf-8'
                        part_detail = parts.json()['data']
                        videoCount = part_detail['total']
                        totalPage = part_detail['total_page']
                        for p in part_detail['list']:
                            if channel_id == 1:
                                part_string = 't4'
                            else:
                                part_string = 't1'
                            if p['isIntact'] == '1':
                                address += ',%s$%s$%s' % (p[part_string], p['t2'], 'https://www.mgtv.com%s' % p['url'])
                    if len(address) > 0:
                        address = address[1:]
                else:
                    span = ''
                    address = '%s$%s$%s' % ('全集', '', 'https://www.mgtv.com%s' % videoDetails1['url'])

                movie = Movie()
                if channel_id == 3:
                    movie.type = 1
                elif channel_id == 2:
                    movie.type = 2
                elif channel_id == 50:
                    movie.type = 3
                elif channel_id == 1:
                    movie.type = 4
                movie.title = name
                movie.span = span
                movie.create_time = createTime
                movie.update_time = updateTime
                movie.address = address
                movie.horizontal = ''
                movie.vertical = img
                movie.actor = mainActors
                movie.child_type = tags
                movie.director = directors
                movie.region = region
                movie.year = year

                movie.total_part = videoCount
                movie.details = desc
                movie.source = 'mgtv'

                # if connection is None:
                #     connection = mysql_connection.get_conn()
                # data_movie.create_movie(connection, movie)
            except:
                print(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        print('end page%d' % i)
    print('end')
