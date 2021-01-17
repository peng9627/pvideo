# coding=utf-8
import traceback

import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys  # 输入框回车
# from selenium.webdriver.common.by import By  # 与下面的2个都是等待时要用到
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException  # 异常处理
# from selenium.webdriver.chrome.options import Options
import re
import os
import json

from pycore.utils.stringutils import StringUtils
from urllib3.exceptions import TimeoutError

reqheaders = {
    "Referer": "https://www.kugou.com/yy/html/search.html",
    'Upgrade-Insecure-Requests': '1',
    'cookie': 'kg_mid=0bc74d97c351a6cc8dd97e611cc3eeb2; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1605269698; kg_dfid=1IMP7Q4GLRXr1737cj1JMz68; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; KuGoo=KugooID=449411081&KugooPwd=8077EECBBBE7D722A3885626F736DE28&NickName=%u0079%u0069%u0031%u0034%u0037%u0030%u0039%u0036%u0032%u0037&Pic=http://imge.kugou.com/kugouicon/165/20130109/20130109192150947980.jpg&RegState=1&RegFrom=&t=312cb753f55dcf27b59cb3ad26f6e0e20759401309bb8af275d2ac31e0f47735&a_id=1014&ct=1605269723&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0034%u0034%u0039%u0034%u0031%u0031%u0030%u0038%u0031; KugooID=449411081; t=312cb753f55dcf27b59cb3ad26f6e0e20759401309bb8af275d2ac31e0f47735; a_id=1014; UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0034%u0034%u0039%u0034%u0031%u0031%u0030%u0038%u0031; mid=0bc74d97c351a6cc8dd97e611cc3eeb2; dfid=1IMP7Q4GLRXr1737cj1JMz68; kg_mid_temp=0bc74d97c351a6cc8dd97e611cc3eeb2; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1605270302',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'}


class KuGou(object):
    def __init__(self):
        pass

    def search(self, song_name):
        data = None
        url = "https://songsearch.kugou.com/song_search_v2?callback=jQuery112407470964083509348_1534929985284&keyword={}&" \
              "page=1&pagesize=10&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filte" \
              "r=0&_=1534929985286".format(song_name)
        try:
            res = requests.get(url).text
            js = json.loads(res[res.index('(') + 1:-2])
            data = js['data']['lists']

        except TimeoutError:
            print("\n网络不佳，请重新下载")
        except:
            print(traceback.format_exc())
            print("未找到资源QAQ")
        return data

    def details(self, fhash, album_id):
        try:
            hash_url = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&album_id=" + album_id + "&hash=" + fhash
            hash_content = requests.get(hash_url, headers=reqheaders).text
            js = json.loads(hash_content)['data']
            play_url = js['play_url'].replace("\\", "")
            lyrics = js['lyrics']
            real_download_url = play_url.replace("\\", "")
        except TimeoutError:
            print("网络不佳，请重新下载")


class QQMusic(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7'
                             '1.0.3578.80 Safari/537.36'}

    def __init__(self):
        pass

    def search(self, song_name):
        data = None
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1' \
              '&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=' + song_name
        try:
            res = requests.get(url).text
            js_of_rest1 = json.loads(res.strip('callback()[]'))
            data = js_of_rest1['data']['song']['list']
        except TimeoutError:
            print("\n网络不佳，请重新下载")
        except:
            print(traceback.format_exc())
            print("未找到资源QAQ")
        return data

    def details(self, song_mid, medias):
        try:
            hash_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=' \
                       '205361747&songmid=' + song_mid + '&filename=C400' + medias + '.m4a&guid=6612300644'
            hash_content = requests.get(hash_url, headers=reqheaders).text
            js = json.loads(hash_content)['data']
            play_url = js['play_url'].replace("\\", "")
            lyrics = js['lyrics']
            real_download_url = play_url.replace("\\", "")
        except TimeoutError:
            print("网络不佳，请重新下载")

    def download(self, data, sing_name):
        try:
            save_path = 'music/' + sing_name + '.m4a'
            true_path = os.path.abspath(save_path)
            try:
                print("下载中.....")
                with open(save_path, 'wb') as f:
                    f.write(data)
                print("{}已下载至{}".format(sing_name, true_path))
            except Exception as err:
                print("文件写入出错:", err)
                return None
        except Exception as er:
            print("文件music找不到\n请重新下载", er)
            return None

    def qq_music_api(self):
        print("\n", "{:^30}".format("正在使用QQ音乐VIP下载器"))
        while True:
            song_name = input("\n请输入歌名>>").strip()
            print("正在努力寻找资源.........")
            if song_name == '':
                continue
            elif song_name == 'q':
                print("退出QQ音乐下载")
                break
            url1 = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1' \
                   '&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=' + song_name
            try:
                rest1 = self.get_request(url1)
                js_of_rest1 = json.loads(rest1.text.strip('callback()[]'))
                js_of_rest1 = js_of_rest1['data']['song']['list']
            except TimeoutError:
                print("网络异常，请重新下载")
                continue
            except:
                print("检测到异常，请重新下载")
                continue
            medias = []
            song_mid = []
            src = []
            song_names = []
            singers = []
            for rest in js_of_rest1:
                try:
                    medias.append(rest['media_mid'])
                    song_mid.append(rest['songmid'])
                    song_names.append(rest['songname'])
                    singers.append(rest['singer'][0]['name'])
                except:
                    print('检测到错误，资源可能与您预期不符')
                    index = input("\n退出下载请按q，继续下载请直接回车>>").strip()
                    if index == 'q':
                        return
                    elif index == '':
                        continue
                    else:
                        print("输入不规范，请重新下载")
                        return

            for n in range(0, len(medias)):
                try:
                    url2 = ''
                    rest2 = self.get_request(url2)
                    js_of_rest2 = json.loads(rest2.text)
                    vkey = js_of_rest2['data']['items'][0]['vkey']
                    src.append(
                        'http://dl.stream.qqmusic.qq.com/C400' + medias[
                            n] + '.m4a?vkey=' + vkey + '&guid=6612300644&uin=0&fromtag=66')
                except TimeoutError:
                    print("网络不佳，请重新下载")
                except:
                    print("检测到异常，请重新下载")
                    break
            print("为你找到以下内容".center(30, '*'))
            print("序号      ", "歌手    -     歌名")
            for m in range(0, len(src)):
                print(str(m + 1) + '    ' + song_names[m] + ' - ' + singers[m] + '.m4a')
            song_index = int(input("请选择序号>>").strip())
            if song_index < 0:
                print("退出QQ音乐下载")
                break
            try:
                song_data = self.get_request(src[song_index - 1])
                data = song_data.content
                self.download(data, song_names[song_index - 1])
            except Exception as er:
                print("检测到异常，请重新下载 ", er)


if __name__ == '__main__':
    # kg_API = KuGou()
    # res = kg_API.search('最爱')
    # fhash = res[0]["FileHash"]
    # AlbumID = res[0]["AlbumID"]
    # kg_API.details(fhash, AlbumID)
    qq_API = QQMusic()
    res = qq_API.search('最爱')
    songmid = res[0]['songmid']
    mediamid = res[0]['media_mid']
    qq_API.details(songmid, mediamid)
