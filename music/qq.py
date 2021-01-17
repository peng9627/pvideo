# -*- coding: utf-8 -*-
import binascii
import codecs
import traceback

import requests
import random
import base64
import json
import os
from Crypto.Cipher import AES
from pycore.utils.stringutils import StringUtils


class QQMusic(object):
    def __init__(self):
        self.ios_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'Referer': 'http://y.qq.com'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Referer': 'http://y.qq.com'
        }
        self.search_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        self.mobile_fcg_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
        self.fcg_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'

    def search(self, song_name):
        data = None
        params = {
            'w': song_name,
            'format': 'json',
            'p': '1',
            'n': '20'
        }
        try:
            response = requests.get(self.search_url, headers=self.headers, params=params)
            data = response.json()['data']['song']['list']
        except:
            print(traceback.format_exc())
            print("未找到资源QAQ")
        return data

    def details(self, id):
        download_url = None
        # params = {
        #     'guid': str(random.randrange(1000000000, 10000000000)),
        #     'cid': '205361747',
        #     'songmid': id,
        #     'format': 'json',
        #     'outCharset': 'utf8',
        #     'uin': '0'
        # }
        # for quality in [("C400", "m4a", 128),
        #                 ("M500", "mp3", 128)]:
        #     params['filename'] = '%s%s.%s' % (quality[0], id, quality[1])
        #     response = requests.get(self.mobile_fcg_url, headers=self.ios_headers, params=params)
        #     response_json = response.json()
        #     if response_json['code'] != 0: continue
        #     vkey = response_json.get('data', {}).get('items', [{}])[0].get('vkey', '')
        #     if vkey:
        #         ext = quality[1]
        #         download_url = 'http://dl.stream.qqmusic.qq.com/{}?vkey={}&guid={}&uin=3051522991&fromtag=64'.format(
        #             '%s%s.%s' % (quality[0], id, quality[1]), vkey, params['guid'])
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        if download_url is None:
            params = {
                '-': 'getplaysongvkey33316352515834',
                'g_tk': '1316931688',
                'format': 'json',
                'outCharset': 'utf8',
                'notice': '0',
                'needNewCode': '0',
                'platform': 'yqq.json',
                'data': json.dumps({
                    "req": {"module": "CDN.SrfCdnDispatchServer", "method": "GetCdnDispatch",
                            "param": {"guid": "3982823384", "calltype": 0, "userip": ""}},
                    "req_0": {"module": "vkey.GetVkeyServer", "method": "CgiGetVkey",
                              "param": {"guid": "3982823384", "songmid": [id], "songtype": [0], "uin": "0",
                                        "loginflag": 1, "platform": "20"}},
                    "comm": {"uin": 0, "format": "json", "ct": 24, "cv": 0}
                })
            }
            params["sign"] = StringUtils.md5("CJBPACrRuNy7" + params["data"]).upper()
            response = requests.get(url, headers=self.ios_headers, params=params)
            response_json = response.json()
            if response_json['code'] == 0 and response_json['req']['code'] == 0 and response_json['req_0']['code'] == 0:
                ext = '.m4a'
                download_url = str(response_json["req"]["data"]["freeflowsip"][0]) + str(
                    response_json["req_0"]["data"]["midurlinfo"][0]["purl"])
        return 1


if __name__ == '__main__':
    qq_api = QQMusic()
    res = qq_api.search('最爱')
    id = res[0]['songmid']
    details = qq_api.details(id)
    print 1
