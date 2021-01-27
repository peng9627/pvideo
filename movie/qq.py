# coding=utf-8
import hashlib
import json
import re
import time
import traceback

import requests
from pyquery import PyQuery

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)  QQLive/10275340/50192209 Chrome/43.0.2357.134 Safari/537.36 QBCore/3.43.561.202 QQBrowser/9.0.2524.400'
}
header_pc = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
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
    videoDetails = requests.get(featurePageUrl, headers=header_pc).text
    vdjss = videoDetails.find('var COVER_INFO = ') + 17
    vdjse = videoDetails.find('var', vdjss)
    vdjs = videoDetails[vdjss:vdjse]
    videoDetailsJson = json.loads(vdjs)

    return videoDetailsJson


def match1(text, *patterns):
    """Scans through a string for substrings matched some patterns (first-subgroups only).
    Args:
        text: A string to be scanned.
        patterns: Arbitrary number of regex patterns.
    Returns:
        When only one pattern is given, returns a string (None if no match found).
        When more than one pattern are given, returns a list of strings ([] if no match found).
    """

    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
        return ret


def play_urls(vid):
    video_json = None
    platforms = [4100201, 11]
    part_urls = []
    for platform in platforms:
        info_api = 'http://vv.video.qq.com/getinfo?otype=json&appver=3.2.19.333&platform={}&defnpayver=1&defn=fhd&vid={}'.format(
            platform, vid)
        info = requests.get(info_api, headers).text
        video_json = json.loads(match1(info, r'QZOutputJson=(.*)')[:-1])
        if not video_json.get('msg') == 'cannot play outside':
            break
    fn_pre = video_json['vl']['vi'][0]['lnk']
    title = video_json['vl']['vi'][0]['ti']
    host = video_json['vl']['vi'][0]['ul']['ui'][0]['url']
    vt = video_json['vl']['vi'][0]['ul']['ui'][0]['vt']
    seg_cnt = fc_cnt = video_json['vl']['vi'][0]['cl']['fc']

    filename = video_json['vl']['vi'][0]['fn']
    if seg_cnt == 0:
        seg_cnt = 1
    else:
        fn_pre, magic_str, video_type = filename.split('.')
    # url1 = video_json['vl']['vi'][0]['ul']['ui'][0]['url'] + video_json['vl']['vi'][0]['fn'] + "?vkey=" + \
    #        video_json['vl']['vi'][0]['fvkey']
    # filename = vid + '.mp4'
    # key_api = 'http://vv.video.qq.com/getkey?format=2&otype=json&vt=150&vid=' + vid + '&ran=0\%2E9477521511726081\\&charge=0&filename=' + filename + '&platform=11'
    # part_info = requests.get(key_api, headers).text
    # key_json = json.loads(match1(part_info, r'QZOutputJson=(.*)')[:-1])
    #
    # url2 = video_json['vl']['vi'][0]['ul']['ui'][0]['url'] + filename + '?vkey=' + key_json['key']
    for fi in video_json['fl']['fi']:
        filename = '%s.p%d.1.mp4' % (vid, fi['id']%10000)
        key_api = "http://vv.video.qq.com/getkey?otype=json&platform=11&format={}&vid={}&filename={}&appver=3.2.19.333".format(
            fi['id'], vid, filename)
        part_info = requests.get(key_api, headers).text
        key_json = json.loads(match1(part_info, r'QZOutputJson=(.*)')[:-1])
        url = '{}{}?vkey={}'.format(host, filename, key_json['key'])
        print(1)

    # part_urls = []
    # total_size = 0
    # for part in range(1, seg_cnt + 1):
    #     if fc_cnt == 0:
    #         # fix json parsing error
    #         part_format_id = video_json['vl']['vi'][0]['cl']['keyid'].split('.')[-1]
    #     else:
    #         part_format_id = video_json['vl']['vi'][0]['cl']['ci'][part - 1]['keyid'].split('.')[1]
    #         filename = '.'.join([fn_pre, magic_str, str(part), video_type])
    #
    #     key_api = "http://vv.video.qq.com/getkey?otype=json&platform=11&format={}&vid={}&filename={}&appver=3.2.19.333".format(
    #         part_format_id, vid, filename)
    #     part_info = requests.get(key_api, headers).text
    #     key_json = json.loads(match1(part_info, r'QZOutputJson=(.*)')[:-1])
    #     if key_json.get('key') is None:
    #         vkey = video_json['vl']['vi'][0]['fvkey']
    #         url = '{}{}?vkey={}'.format(video_json['vl']['vi'][0]['ul']['ui'][0]['url'], fn_pre + '.mp4', vkey)
    #     else:
    #         vkey = key_json['key']
    #         url = '{}{}?vkey={}'.format(host, filename, vkey)
    #     if not vkey:
    #         if part == 1:
    #             print(key_json['msg'])
    #         else:
    #             print(key_json['msg'])
    #         break
    #     if key_json.get('filename') is None:
    #         print(key_json['msg'])
    #         break
    #     part_urls.append(url)

    print('end')


if __name__ == '__main__':
    # ss = get_details('https://v.qq.com/x/cover/mzc002002vcxot9/c0035cn9yyf.html')
    play_urls('c0035cn9yyf')
    print('1')
