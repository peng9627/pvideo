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
    channel_id = 96  # 1.96 2.97 3.100 4.85
    url = 'https://www.youku.com/category/page?c=%d&s=6&type=show&p=%d'
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9',
        'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'cookie': 'UM_distinctid=17723ea61d12b6-04eb0508ca18d7-31346d-1fa400-17723ea61d25d6; cna=wx+QGPT+gTECAWpUEejmGDWD; __ysuid=1611215299799gAM; __aysid=16112152998029VG; __ayft=1611215299802; __ayscnt=1; xlly_s=1; csrfToken=c0rwd3vyIFarYeH4eHkHrfhc; redMarkRead=1; __wpkreporterwid_=d025bdd0-20f5-4f51-8ad9-74ae760b4255; CNZZDATA1277956573=2135599496-1611210158-https%253A%252F%252Fwww.youku.com%252F%7C1611220958; modalFrequency={"UUID":"2"}; CNZZDATA1277956656=556303090-1611213292-https%253A%252F%252Ftv.youku.com%252F%7C1611234892; __arycid=dd-3-00; __arcms=dd-3-00; __arpvid=1611240993213Fp3EMa-1611240993234; __aypstp=117; __ayspstp=117; P_ck_ctl=4BE1F96A72B7324A871B522764E0F183; _m_h5_tk=5fa55ffe9d35576360e41f95669f89e1_1611245195073; _m_h5_tk_enc=8d086d745b8b31222e99a4ff1a530bfc; __ayvstp=44; __aysvstp=44; l=eBNqsOQrjjHGC2oFBO5CFurza779qIRbzsPzaNbMiInca6gCtFZt6OCI194kSdtj_t5D2etzLAUwVR3y7WzLRxZDWHVgPr_AZaJ68e1..; tfstk=c3vfBpTEEr4jMnha3niz3mwrduXNCvqCfj_DcIzIXyeQdXrAyR1c6J7IYQAgW8CdV; isg=BG1tOtKR8cUNVJWpLuwbnOoRfAnnyqGcCLhcoq9yaoR4Jo_Ydxl4bBOwEPLAprlU'
    }
    header_pc = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://www.youku.com/category/show/c_96.html',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'UM_distinctid=17723ea61d12b6-04eb0508ca18d7-31346d-1fa400-17723ea61d25d6; cna=wx+QGPT+gTECAWpUEejmGDWD; __ysuid=1611215299799gAM; __aysid=16112152998029VG; __ayft=1611215299802; __ayscnt=1; xlly_s=1; csrfToken=c0rwd3vyIFarYeH4eHkHrfhc; redMarkRead=1; __wpkreporterwid_=d025bdd0-20f5-4f51-8ad9-74ae760b4255; CNZZDATA1277956573=2135599496-1611210158-https%253A%252F%252Fwww.youku.com%252F%7C1611220958; modalFrequency={"UUID":"2"}; CNZZDATA1277956656=556303090-1611213292-https%253A%252F%252Ftv.youku.com%252F%7C1611234892; __arycid=dd-3-00; __arcms=dd-3-00; __arpvid=1611240993213Fp3EMa-1611240993234; __aypstp=117; __ayspstp=117; P_ck_ctl=4BE1F96A72B7324A871B522764E0F183; _m_h5_tk=5fa55ffe9d35576360e41f95669f89e1_1611245195073; _m_h5_tk_enc=8d086d745b8b31222e99a4ff1a530bfc; __ayvstp=44; __aysvstp=44; l=eBNqsOQrjjHGC2oFBO5CFurza779qIRbzsPzaNbMiInca6gCtFZt6OCI194kSdtj_t5D2etzLAUwVR3y7WzLRxZDWHVgPr_AZaJ68e1..; tfstk=c3vfBpTEEr4jMnha3niz3mwrduXNCvqCfj_DcIzIXyeQdXrAyR1c6J7IYQAgW8CdV; isg=BG1tOtKR8cUNVJWpLuwbnOoRfAnnyqGcCLhcoq9yaoR4Jo_Ydxl4bBOwEPLAprlU'
    }
    for i in range(1, 2):
        url1 = url % (channel_id, i)
        response = requests.get(url1, headers=header_pc)
        response.encoding = 'utf-8'
        videos = response.json()['data']
        for v in videos:
            connection = None
            try:
                year = 1970
                pageUrl = 'https://m.youku.com/video/id_%s.html' % v['videoId']
                img = 'https:%s' % v['img']
                name = v['title']
                span = v['summary']
                videoDetails1 = requests.get(pageUrl, headers=header)
                videoDetails1.encoding = 'utf-8'
                videoDetails1 = videoDetails1.text
                vdjss = videoDetails1.find('__INITIAL_DATA__ =') + 18
                vdjse = videoDetails1.find(';window.__PLATOCONFIG__', vdjss)
                vdjs = videoDetails1[vdjss:vdjse]
                videoDetailsJson = json.loads(vdjs)
                desc = ''
                region = '其他'
                directors = ''
                mainActors = ''
                address = ''
                tags = ''
                videoCount = videoDetailsJson['videoMap']['episodeTotal']
                createTime = int(time.time())
                if 96 == channel_id:
                    address += ',%s$%s$%s' % ('全集', '', pageUrl)
                for v in videoDetailsJson['componentList']:
                    if v['type'] == 10009:
                        for n in v['dataNode']:
                            if n['type'] == 10010:
                                region = n['data']['area'][0]
                                year = n['data']['showReleaseYear']
                                desc = n['data']['desc']
                                if 'showGenre' in n['data']:
                                    tags = n['data']['showGenre'].replace(' ', ',')
                                if 96 == channel_id:
                                    span = n['data']['doubanRate']
                            elif n['type'] == 10011:
                                if 'subtitle' in n['data'] and '导演' == n['data']['subtitle']:
                                    directors += ',' + n['data']['title']
                                else:
                                    mainActors += ',' + n['data']['title']
                    elif v['type'] == 10013 and channel_id != 96:
                        for n in v['dataNode']:
                            if n['data']['videoType'] == '正片':
                                address += ',%d$%s$%s' % (n['data']['stage'], n['data']['title'],
                                                          'https://m.youku.com/video/id_%s.html' % n['data']['action'][
                                                              'value'])
                if len(directors) > 0:
                    directors = directors[1:]
                if len(mainActors) > 0:
                    mainActors = mainActors[1:]
                if len(address) > 0:
                    address = address[1:]
                updateTime = int(time.time())
                if desc is None:
                    desc = name

                movie = Movie()
                if channel_id == 96:
                    movie.type = 1
                elif channel_id == 97:
                    movie.type = 2
                elif channel_id == 100:
                    movie.type = 3
                elif channel_id == 85:
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
                movie.source = 'youku'

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
