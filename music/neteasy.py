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


class Cracker():
    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'

    def get(self, text):
        text = json.dumps(text)
        secKey = self._createSecretKey(16)
        encText = self._aesEncrypt(self._aesEncrypt(text, self.nonce), secKey)
        encSecKey = self._rsaEncrypt(secKey, self.pubKey, self.modulus)
        post_data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        return post_data

    def _aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        text = text + str(pad * chr(pad))
        secKey = secKey.encode('utf-8')
        encryptor = AES.new(secKey, 2, b'0102030405060708')
        text = text.encode('utf-8')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def _rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def _createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]


class WangYiYunMusic(object):
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Origin': 'https://music.163.com',
            'Referer': 'https://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.32 Safari/537.36'
        }

    def search(self, song_name):
        id_url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        data = None
        params = {
            's': song_name,
            'type': '1',
            'offset': '0',
            'sub': 'false',
            'limit': '20'
        }
        try:
            response = requests.post(id_url, headers=self.headers, params=params, data=Cracker().get(params))
            js = response.json()
            data = js['result']['songs']
        except:
            print(traceback.format_exc())
            print("未找到资源QAQ")
        return data

    def details(self, id, br):
        player_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        params = {
            'ids': [int(id)],
            'br': int(br),
            'csrf_token': ''
        }
        response = requests.post(player_url, headers=self.headers, data=Cracker().get(params))
        return response.json()


if __name__ == '__main__':
    wyy_api = WangYiYunMusic()
    res = wyy_api.search('最爱')
    id = res[0]['id']
    br = res[0]['h']['br']
    details = wyy_api.details(id, br)
    print 1
