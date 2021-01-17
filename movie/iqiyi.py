# coding=utf-8
import hashlib
import json
import time
import traceback

import requests
from pyquery import PyQuery

header = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
    'referer': 'https://m.iqiyi.com/'
}
header_pc = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
}


def getVMS(tvid, vid):
    t = int(time.time() * 1000)
    src = '76f90cbd92f94a2e925d83e8ccd22cb7'
    key = 'd5fb4bd9d50c4be6948c97edd7254b0e'
    sc = hashlib.new('md5', bytes(str(t) + key + vid)).hexdigest()
    vmsreq = 'http://cache.m.iqiyi.com/tmts/{0}/{1}/?t={2}&sc={3}&src={4}'.format(tvid, vid, t, sc, src)
    return requests.get(vmsreq, headers=header_pc).json()


def get_details(url):
    featurePageUrl = url.replace("://m.", "://")
    videoDetails1 = requests.get(featurePageUrl, headers=header_pc).text
    d = PyQuery(videoDetails1)
    ss = d("div").filter('.episodeIntro-item').children()
    region = '其它'
    year = 1970
    for s in ss:
        sitem = PyQuery(s)
        if sitem('span').text() == u'年份：':
            year = sitem('a:first').text()
        elif sitem('span').text() == u'地区：':
            region = sitem('a:first').text()
    videoDetails = requests.get(url, headers=header).text
    vdjss = videoDetails.find('<script>window.__INITIAL_STATE__=') + 33
    vdjse = videoDetails.find(';(function()', vdjss)
    vdjs = videoDetails[vdjss:vdjse]
    videoDetailsJson = json.loads(vdjs)["play"]
    videoDetailsJson["region"] = region
    videoDetailsJson["year"] = year
    return videoDetailsJson


def get_address(albumId):
    address = ''
    page = 1
    url2 = 'https://pub.m.iqiyi.com/h5/main/videoList/album/?albumId=%d&size=20&page=%d&needPrevue=true&needVipPrevue=false'
    while True:
        response1 = requests.get(url2 % (albumId, page), headers=header)
        restext = response1.json()
        for vv in restext['data']['videos']:
            year = vv['year']
            if vv['type'] == 1:
                address += ',%s$%s$%s' % (str(vv['pd']), vv['vt'], vv['pageUrl'])
        totalPages = restext["data"]["totalPages"]
        if totalPages == page:
            break
        page += 1
    return address


def play_urls(tvid, vid):
    info = getVMS(tvid, vid)
    stream_types = [
        {'id': '4k', 'container': 'm3u8', 'video_profile': '4k'},
        {'id': 'BD', 'container': 'm3u8', 'video_profile': '1080p'},
        {'id': 'TD', 'container': 'm3u8', 'video_profile': '720p'},
        {'id': 'TD_H265', 'container': 'm3u8', 'video_profile': '720p H265'},
        {'id': 'HD', 'container': 'm3u8', 'video_profile': '540p'},
        {'id': 'HD_H265', 'container': 'm3u8', 'video_profile': '540p H265'},
        {'id': 'SD', 'container': 'm3u8', 'video_profile': '360p'},
        {'id': 'LD', 'container': 'm3u8', 'video_profile': '210p'},
    ]
    vd_2_id = {10: '4k', 19: '4k', 5: 'BD', 18: 'BD', 21: 'HD_H265', 2: 'HD', 75: 'HD', 4: 'TD', 17: 'TD_H265',
               96: 'LD', 1: 'SD', 14: 'TD'}
    id_2_profile = {'4k': '4k', 'BD': '1080p', 'TD': '720p', 'HD': '540p', 'SD': '360p', 'LD': '210p',
                    'HD_H265': '540p H265', 'TD_H265': '720p H265'}
    streams = {}
    for stream in info['data']['vidl']:
        try:
            stream_id = vd_2_id[stream['vd']]
            if stream_id in stream_types:
                continue
            stream_profile = id_2_profile[stream_id]
            streams[stream_id] = {'video_profile': stream_profile, 'container': 'm3u8', 'src': [stream['m3u']],
                                  'size': 0, 'm3u8_url': stream['m3u']}
        except:
            print traceback.format_exc()
    return streams


if __name__ == '__main__':
    ss = get_details('https://m.iqiyi.com/v_18schl0tktg.html')
    addr = get_address(ss['videoInfo']['aid'])
    play_urls = play_urls(ss['videoInfo']['tvid'], ss['videoInfo']['vid'])
    print 1
