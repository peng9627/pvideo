# coding=utf-8
import json
import time
import traceback

import requests
from pycore.data.entity import config, globalvar as gl
from pycore.utils import time_utils

config.init("./conf/pyg.conf")
gl.init()

from pycore.data.database import mysql_connection
from pyquery import PyQuery

from data.database import data_movie
from mode.movie import Movie

if __name__ == '__main__':
    channel_id = 'movie'  # movie tv  variety cartoon
    url = 'https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=%s&feature=-1&listpage=%d&offset=%d&pagesize=100&sort=18'
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    header_pc = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    for i in range(1, 2):
        url1 = url % (channel_id, i, (i - 1) * 100)
        response = requests.get(url1, headers=header_pc)
        response.encoding = 'utf-8'
        datas = PyQuery(response.text)
        videos = datas('div').filter('.list_item')
        for v in videos:
            connection = None
            try:
                year = 1970
                videosData = PyQuery(v)
                pageUrl = videosData('a:first').attr('href')
                img = 'https:%s' % videosData('a:first').children('img').attr('src')
                name = videosData('div').filter('.figure_detail_two_row').children('a:first').text()
                span = videosData('div').filter('.figure_caption').text()
                videoDetails1 = requests.get(pageUrl, headers=header_pc)
                videoDetails1.encoding = 'utf-8'
                videoDetails1 = videoDetails1.text
                vdjss = videoDetails1.find('COVER_INFO = ') + 13
                vdjse = videoDetails1.find('var ', vdjss)
                vdjs = videoDetails1[vdjss:vdjse]
                videoDetailsJson = json.loads(vdjs)
                region = videoDetailsJson['area_name']
                if len(videoDetailsJson["publish_date"]) > 0:
                    createTime = time_utils.string_to_stamp(videoDetailsJson["publish_date"], '%Y-%m-%d')
                else:
                    createTime = 0
                updateTime = int(time.time())
                desc = videoDetailsJson["description"]
                if desc is None:
                    desc = name
                year = videoDetailsJson['year']
                tags = videoDetailsJson['main_genre']
                if 'sub_genre' in videoDetailsJson:
                    sub_genre = videoDetailsJson['sub_genre']
                    if sub_genre is not None and len(sub_genre) > 0:
                        tags += ',' + ','.join(videoDetailsJson['sub_genre'])
                episode_all = videoDetailsJson['episode_all']
                if episode_all is not None and len(episode_all) > 0:
                    videoCount = int(episode_all)
                else:
                    videoCount = 0
                if 'movie' == channel_id:
                    directors = ''
                    if 'director' in videoDetailsJson and videoDetailsJson['director'] is not None:
                        directors = ','.join(videoDetailsJson['director'])
                    mainActors = ''
                    if 'leading_actor' in videoDetailsJson and videoDetailsJson['leading_actor'] is not None:
                        mainActors = ','.join(videoDetailsJson['leading_actor'])
                    address = '%s$%s$%s' % (u'全集', '', pageUrl)
                    span = u'%s分' % videoDetailsJson['score']['score']
                elif 'variety' == channel_id:
                    column_id = videoDetailsJson['column_id']
                    offset = 0
                    total = 21
                    address = ''
                    while offset < total:
                        time.sleep(0.2)
                        parts = requests.get(
                            'https://list.video.qq.com/fcgi-bin/list_common_cgi?otype=json&novalue=1&nounion=0&platform=1&version=10000&intfname=web_integrated_lid_list&tid=543&appkey=ebe7ee92f568e876&appid=20001174&sourceid=10001&listappid=10385&listappkey=10385&playright=2&sourcetype=1&cidorder=1&locate_type=0&lid=%d&pagesize=20&offset=%d&_=%d' % (
                                column_id, offset, int(time.time() * 1000)), headers=header_pc).text
                        partjson = json.loads(parts[parts.find('=') + 1:-1])
                        if 'results' in partjson['jsonvalue']:
                            total = partjson['total']
                            offset += 20
                            for p in partjson['jsonvalue']['results']:
                                address += u',%s期$%s$%s' % (
                                    p['fields']['publish_date'], p['fields']['c_second_title'],
                                    pageUrl.replace('.html', '/%s.html' % p['id']))
                                try:
                                    if p['fields']['publish_date'].find(':') != -1:
                                        createTime = time_utils.string_to_stamp(p['fields']['publish_date'],
                                                                                '%Y-%m-%d %H:%M:%S')
                                    else:
                                        createTime = time_utils.string_to_stamp(p['fields']['publish_date'],
                                                                                '%Y-%m-%d')
                                except:
                                    print 1
                        else:
                            print 1
                    if len(year) == 0:
                        year = int(time_utils.stamp_to_string(createTime, '%Y'))
                    directors = ''
                    mainActors = ''
                    if 'guests' in videoDetailsJson and videoDetailsJson['guests'] is not None:
                        mainActors = ','.join(videoDetailsJson['guests'])
                else:
                    directors = ''
                    if 'director' in videoDetailsJson and videoDetailsJson['director'] is not None:
                        directors = ','.join(videoDetailsJson['director'])
                    mainActors = ''
                    if 'leading_actor' in videoDetailsJson and videoDetailsJson['leading_actor'] is not None:
                        mainActors = ','.join(videoDetailsJson['leading_actor'])
                    id = pageUrl.split('/')[-1][:-5]
                    address = ''
                    parturl = 'https://s.video.qq.com/get_playsource?id=%s&type=4&range=%s&plname=qq&otype=json&_t=%d'
                    parts = requests.get(parturl % (id, '1-1', int(time.time() * 1000)), headers=header_pc).text
                    partjson = json.loads(parts[parts.find('=') + 1:-1])
                    indexList = partjson['PlaylistItem']['indexList']
                    for r in indexList:
                        time.sleep(0.2)
                        parts = requests.get(parturl % (id, r, int(time.time() * 1000)), headers=header_pc).text
                        partjson = json.loads(parts[parts.find('=') + 1:-1])
                        if 'PlaylistItem' in partjson and partjson[
                            'PlaylistItem'] is not None and 'videoPlayList' in partjson['PlaylistItem'] and \
                                partjson['PlaylistItem']['videoPlayList'] is not None:
                            for p in partjson['PlaylistItem']['videoPlayList']:
                                address += ',%s$%s$%s' % (p['episode_number'], p['title'], p['playUrl'])
                        else:
                            print 1
                    if len(address) > 0:
                        address = address[1:]

                movie = Movie()
                if channel_id == 'tv':
                    movie.type = 2
                elif channel_id == 'cartoon':
                    movie.type = 3
                elif channel_id == 'variety':
                    movie.type = 4
                elif channel_id == 'movie':
                    movie.type = 1
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
                movie.source = 'qq'

                # if connection is None:
                #     connection = mysql_connection.get_conn()
                # data_movie.create_movie(connection, movie)
            except:
                print traceback.format_exc()
            finally:
                if connection is not None:
                    connection.close()
        print 'end page%d' % i
    print 'end'
