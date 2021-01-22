# coding=utf-8
import json
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
    channel_id = 1  # channel_id=1电影2电视剧6综艺4动漫
    url = 'https://pub.m.iqiyi.com/h5/main/recVideos/lib/?page_id=%d&mode=24&channel_id=%d&smart_tag=&three_category_id=&content_type=&is_purchase=&ret_num=100&pos=1&type=list&market_release_date_level=-&post=list&from=mobile_videolib&is_unified_interface=1&version=1.0.0&device_id=7vu9385vytkuju1oxikxm2&play_platform=H5_QIYI&passport_id=&session='
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        'referer': 'https://m.iqiyi.com/'
    }
    header_pc = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
    }
    for i in range(1, 2):
        url1 = url % (i, channel_id)
        response = requests.get(url1, headers=header)
        data = response.json()
        videos = data['data']['videos']
        for v in videos:
            connection = None
            try:
                year = 1970
                if 1 == channel_id:
                    featurePageUrl = v['pageUrl'].replace("//m.", "//")
                    videoDetails1 = requests.get("https:%s" % featurePageUrl, headers=header_pc).text
                    vdjss = videoDetails1.find(':video-info=\'') + 13
                    vdjse = videoDetails1.find('\'>', vdjss)
                    vdjs = videoDetails1[vdjss:vdjse]
                    videoDetailsJson = json.loads(vdjs)
                    name = videoDetailsJson['name']
                    if 'areas' in videoDetailsJson and len(videoDetailsJson['areas']) > 0:
                        region = videoDetailsJson['areas'][0]
                    else:
                        region = '其它'
                    createTime = videoDetailsJson["firstPublishTime"]
                    updateTime = videoDetailsJson["lastPublishTime"]
                    img = videoDetailsJson["posterUrl"]
                    videoCount = 1
                    desc = videoDetailsJson["description"]
                    span = videoDetailsJson["score"]
                    directors = ''
                    mainActors = ''
                    tags = ''
                    if 'cast' in videoDetailsJson:
                        if 'directors' in videoDetailsJson['cast']:
                            for d in videoDetailsJson['cast']['directors']:
                                directors += ',%s' % d['name']
                        if 'mainActors' in videoDetailsJson['cast']:
                            for d in videoDetailsJson['cast']['mainActors']:
                                mainActors += ',%s' % d['name']
                    if 'categories' in videoDetailsJson:
                        for d in videoDetailsJson['categories']:
                            if d['subName'] == u'类型':
                                tags += ',%s' % d['name']
                    if len(directors) > 0:
                        directors = directors[1:]
                    if len(mainActors) > 0:
                        mainActors = mainActors[1:]
                    if len(tags) > 0:
                        tags = tags[1:]

                    d = PyQuery(videoDetails1)
                    ss = d("ul").filter('.vInfoSide_ul').children()
                    address = '%s$%s$%s' % ('', '', videoDetailsJson['url'])
                    for s in ss:
                        sitem = PyQuery(s)
                        if sitem('em:first').text() == u'首映：':
                            year = sitem('span').filter('.start_nameTxt').text()
                elif 2 == channel_id:
                    albumId = v['albumId']
                    name = v['albumName']
                    img = v['albumImageUrl']
                    featurePageUrl = v['kvs']['featurePageUrl'].replace("//m.", "//")
                    videoDetails1 = requests.get("https:%s" % featurePageUrl, headers=header_pc).text
                    d = PyQuery(videoDetails1)
                    ss = d("div").filter('.episodeIntro-item').children()
                    region = '其它'
                    tags = ''
                    for s in ss:
                        sitem = PyQuery(s)
                        if sitem('span').text() == u'类型：':
                            for tg in sitem('a'):
                                t = PyQuery(tg)
                                if len(t.attr('href')) > 0 and t.attr('href').find('javascript') == -1:
                                    tags += ',%s' % t.text()
                            if len(tags) > 0:
                                tags = tags[1:]
                        elif sitem('span').text() == u'年份：':
                            year = sitem('a:first').text()
                        elif sitem('span').text() == u'地区：':
                            region = sitem('a:first').text()
                    desst = videoDetails1.find('<div class="episodeIntro-brief" title="') + 39
                    desed = videoDetails1.find('"', desst)
                    desc = videoDetails1[desst:desed]

                    vdjss = videoDetails1.find('id="album-avlist-data" value=\'') + 30
                    vdjse = videoDetails1.find('\'/>', vdjss)
                    vdjs = videoDetails1[vdjss:vdjse]
                    videoDetailsJson = json.loads(vdjs)
                    videoCount = videoDetailsJson['videoCount']
                    createTime = None
                    updateTime = None
                    directors = None
                    mainActors = None
                    address = ''
                    if videoDetailsJson['latestOrder'] == videoCount:
                        span = '%d集全' % videoCount
                    else:
                        span = '更新至%d集/共%d集' % (videoDetailsJson['latestOrder'], videoCount)
                    for p in videoDetailsJson['epsodelist']:
                        address += ',%d$%s$%s' % (p['order'], p['subtitle'] if 'subtitle' in p else '', p['playUrl'])
                        if createTime is None:
                            createTime = p['issueTime']
                        updateTime = p['issueTime']
                        if directors is None:
                            if 'director' in p['people']:
                                directors = ''
                                for dir in p['people']['director']:
                                    directors += ',%s' % dir['name']
                                if len(directors) > 0:
                                    directors = directors[1:]
                        if mainActors is None:
                            if 'main_charactor' in p['people']:
                                mainActors = ''
                                for mc in p['people']['main_charactor']:
                                    mainActors += ',%s' % mc['name']
                                if len(mainActors) > 0:
                                    mainActors = mainActors[1:]
                    if len(address) > 0:
                        address = address[1:]
                elif channel_id == 6:
                    albumId = v['albumId']
                    name = v['albumName']
                    img = v['albumImageUrl']
                    featurePageUrl = v['pageUrl'].replace("//m.", "//")
                    videoDetails1 = requests.get("https:%s" % featurePageUrl, headers=header_pc).text
                    vdjss = videoDetails1.find(':video-info=\'') + 13
                    vdjse = videoDetails1.find('\'>', vdjss)
                    vdjs = videoDetails1[vdjss:vdjse]
                    videoDetailsJson = json.loads(vdjs)
                    if 'areas' in videoDetailsJson and len(videoDetailsJson['areas']) > 0:
                        region = videoDetailsJson['areas'][0]
                    else:
                        region = '其它'
                    createTime = videoDetailsJson["firstPublishTime"]
                    updateTime = videoDetailsJson["lastPublishTime"]
                    videoCount = 0
                    span = u'更新至%s期' % videoDetailsJson['period']
                    directors = ''
                    mainActors = ''
                    tags = ''
                    if 'cast' in videoDetailsJson:
                        if 'hosts' in videoDetailsJson['cast']:
                            for d in videoDetailsJson['cast']['hosts']:
                                mainActors += ',%s' % d['name']
                    if 'categories' in videoDetailsJson:
                        for d in videoDetailsJson['categories']:
                            if d['subName'] == u'类型':
                                tags += ',%s' % d['name']
                    if len(mainActors) > 0:
                        mainActors = mainActors[1:]
                    if len(tags) > 0:
                        tags = tags[1:]

                    if 'album' in videoDetailsJson:
                        name = videoDetailsJson['album']['name']
                        desc = videoDetailsJson['album']["description"]
                    else:
                        name = ''
                        desc = ''
                        print('error')

                    tvid = videoDetailsJson['tvId']
                    date = time_utils.stamp_to_string(updateTime / 1000, '%Y%m%d')
                    address = ''
                    while True:
                        videoDetailsJson = requests.get(
                            "https://pcw-api.iqiyi.com/album/source/listByNumber/%d?date=%s&include=false&number=10&seq=true&tvId=%d" % (
                                albumId, date, tvid), headers=header_pc).json()
                        if 'data' not in videoDetailsJson:
                            print('error')
                            break
                        for p in videoDetailsJson['data']:
                            date = time_utils.stamp_to_string(p['firstPublishTime'] / 1000, '%Y%m%d')
                            tvid = p['tvId']
                            address += ',%s$%s$%s' % (
                                date, p['subtitle'] if 'subtitle' in p else '', p['url'])
                        if len(videoDetailsJson) < 10:
                            break
                    if len(address) > 0:
                        address = address[1:]
                    if year == 1970:
                        year = int(time_utils.stamp_to_string(createTime / 1000, '%Y'))

                else:
                    albumId = v['albumId']
                    if 'featurePageUrl' in v['kvs']:
                        name = v['albumName']
                        img = v['albumImageUrl']
                        featurePageUrl = v['kvs']['featurePageUrl'].replace("//m.", "//")
                        videoDetails1 = requests.get("https:%s" % featurePageUrl, headers=header_pc).text
                        d = PyQuery(videoDetails1)
                        ss = d("div").filter('.episodeIntro-item').children()
                        region = '其它'
                        tags = ''
                        for s in ss:
                            sitem = PyQuery(s)
                            if sitem('span').text() == u'类型：':
                                for tg in sitem('a'):
                                    t = PyQuery(tg)
                                    if len(t.attr('href')) > 0 and t.attr('href').find('javascript') == -1:
                                        tags += ',%s' % t.text()
                                if len(tags) > 0:
                                    tags = tags[1:]
                            elif sitem('span').text() == u'年份：':
                                year = sitem('a:first').text()
                            elif sitem('span').text() == u'地区：':
                                region = sitem('a:first').text()
                        desst = videoDetails1.find('<div class="episodeIntro-brief" title="') + 39
                        desed = videoDetails1.find('"', desst)
                        desc = videoDetails1[desst:desed]

                        videoCount = 0
                        createTime = None
                        updateTime = None
                        directors = ''
                        mainActors = ''
                        address = ''
                        page = 0
                        totalPage = 1
                        span = ''
                        while page < totalPage:
                            page += 1
                            videoDetailsJson = requests.get(
                                "https://pcw-api.iqiyi.com/albums/album/avlistinfo?aid=%d&size=100&page=%d" % (
                                    albumId, page), headers=header_pc).json()['data']
                            videoCount = videoDetailsJson['videoCount']
                            totalPage = videoDetailsJson['page']
                            if videoDetailsJson['latestOrder'] == videoCount:
                                span = '%d集全' % videoCount
                            elif 0 == videoCount:
                                span = '更新至%d集' % videoDetailsJson['latestOrder']
                            else:
                                span = '更新至%d集/共%d集' % (videoDetailsJson['latestOrder'], videoCount)
                            for p in videoDetailsJson['epsodelist']:
                                address += ',%d$%s$%s' % (
                                    p['order'], p['subtitle'] if 'subtitle' in p else '', p['playUrl'])
                                if createTime is None:
                                    createTime = p['issueTime']
                                updateTime = p['issueTime']
                        if len(address) > 0:
                            address = address[1:]
                    else:
                        img = v['qualityImageUrl']
                        name = v['vt']
                        featurePageUrl = v['pageUrl'].replace("//m.", "//")
                        videoDetails1 = requests.get("https:%s" % featurePageUrl, headers=header_pc).text
                        vdjss = videoDetails1.find(':video-info=\'') + 13
                        vdjse = videoDetails1.find('\'>', vdjss)
                        vdjs = videoDetails1[vdjss:vdjse]
                        videoDetailsJson = json.loads(vdjs)
                        if 'areas' in videoDetailsJson and len(videoDetailsJson['areas']) > 0:
                            region = videoDetailsJson['areas'][0]
                        else:
                            region = '其它'
                        createTime = videoDetailsJson["firstPublishTime"]
                        updateTime = videoDetailsJson["lastPublishTime"]
                        desc = videoDetailsJson["description"]
                        tags = ''
                        if 'categories' in videoDetailsJson:
                            for d in videoDetailsJson['categories']:
                                if d['subName'] == u'类型':
                                    tags += ',%s' % d['name']
                        if len(tags) > 0:
                            tags = tags[1:]
                        else:
                            for d in videoDetailsJson['categories']:
                                if d['subName'] == u'新类型':
                                    tags += ',%s' % d['name']
                        if len(tags) > 0:
                            tags = tags[1:]

                        d = PyQuery(videoDetails1)
                        ss = d("ul").filter('.vInfoSide_ul').children()
                        address = '%s$%s$%s' % ('', '', videoDetailsJson['url'])
                        for s in ss:
                            sitem = PyQuery(s)
                            if sitem('em:first').text() == u'首映：':
                                year = sitem('span').filter('.start_nameTxt').text()
                        if year == 1970:
                            year = int(time_utils.stamp_to_string(createTime / 1000, '%Y'))
                        videoCount = 0
                        directors = ''
                        mainActors = ''
                        address = '%s$%s$%s' % ('', '', videoDetailsJson['url'])
                        span = '全集'

                movie = Movie()
                if channel_id == 6:
                    movie.type = 4
                elif channel_id == 4:
                    movie.type = 3
                else:
                    movie.type = channel_id
                movie.title = name
                movie.span = span
                movie.create_time = createTime / 1000
                movie.update_time = updateTime / 1000
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
                movie.source = 'iqiyi'

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
