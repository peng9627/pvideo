import base64
import json
import time
import traceback
from urllib import parse

import requests
from pycore.data.database import mysql_connection
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from data.database import data_vip_video_url

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
}


def getadd1(addr):
    vdjs = ''
    try:
        result = requests.get('https://vip.laobandq.com/jiexi.php?url=' + addr, headers=headers, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse]
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd2(addr):
    vdjs = ''
    try:
        result = requests.get('https://api.v6.chat/api.php?url=' + parse.quote(addr), headers=headers, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd3(addr):
    vdjs = ''
    try:
        result = requests.get('https://jx.ap2p.cn/jh/jiexi/?url=' + addr, headers=headers, timeout=10).text
        vdjss = result.find('"url": "') + 8
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse]
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd4(addr):
    vdjs = ''
    try:
        datas = {'url': addr, 'referer': '', 'ref': 'false', 'time': '1611645821', 'type': '',
                 'other': str(base64.b64encode(addr.encode("utf-8"))), 'ios': ''}
        result = requests.post('https://ckplayer.gdkaman.com/jiexi/api.php', headers=headers, data=datas,
                               timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd5(addr):
    vdjs = ''
    try:
        datas = {'url': addr, 'referer': '', 'ref': 'false', 'time': '1611645821', 'type': '',
                 'other': str(base64.b64encode(addr.encode("utf-8"))), 'ios': ''}
        result = requests.post('http://5.nmgbq.com/2/api.php', headers=headers, data=datas, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd7(addr):
    vdjs = ''
    try:
        result = requests.get('https://by.98a.ink/api.php?url=' + parse.quote(addr), headers=headers, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd10(addr):
    vdjs = ''
    try:
        result = requests.get('https://jx.rdhk.net/api.php?url=' + parse.quote(addr), headers=headers, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadds(addr):
    connection = None
    url = ''
    try:
        connection = mysql_connection.get_conn()
        parse_urls = data_vip_video_url.query(connection)
        for p in parse_urls:
            if p.name == '1':
                url = getadd1(addr)
            elif p.name == '2':
                url = getadd2(addr)
            elif p.name == '3':
                url = getadd3(addr)
            elif p.name == '4':
                url = getadd4(addr)
            elif p.name == '5':
                url = getadd5(addr)
            elif p.name == '7':
                url = getadd7(addr)
            elif p.name == '10':
                url = getadd10(addr)
            else:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--headless')  # 无界面
                chrome_options.add_argument("--incognito")
                chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在报错问题
                chrome_options.add_argument('--disable-gpu')  # 禁用GPU硬件加速。如果软件渲染器没有就位，则GPU进程将不会启动。
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
                chrome_options.add_argument(
                    'User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36')
                prefs = {"profile.managed_default_content_settings.images": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                # 核心代码
                chrome_options.add_experimental_option('w3c', False)
                caps = DesiredCapabilities.CHROME
                caps['loggingPrefs'] = {'performance': 'ALL'}
                # 核心代码结束
                driver = webdriver.Chrome('D:/software/phantomjs/bin/chromedriver.exe', desired_capabilities=caps,
                                          options=chrome_options)
                try:
                    driver.get('https://jx.youyitv.com/pp/?url=' + addr)
                    t = 10
                    li = 0
                    find = False
                    while t > 0:
                        time.sleep(0.5)
                        log = driver.get_log('performance')
                        for i in range(li, len(log)):
                            s = log[i]['message']
                            if s.find(".m3u8") != -1:
                                message_obj = json.loads(s)
                                if 'request' in message_obj['message']['params']:
                                    url = message_obj['message']['params']['request']['url']
                                find = True
                                break
                        if find:
                            break
                        t -= 1
                        li = len(log)
                except:
                    print(traceback.format_exc())
                finally:
                    driver.quit()
            if len(url) > 0 and 'm3u8' in url:
                break
    except:
        print(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return url


def check_adds(addr):
    connection = None
    try:
        connection = mysql_connection.get_conn()
        parse_urls = data_vip_video_url.query(connection)
        for p in parse_urls:
            url = ''
            times = time.time() * 1000
            if p.name == '1':
                url = getadd1(addr)
            elif p.name == '2':
                url = getadd2(addr)
            elif p.name == '3':
                url = getadd3(addr)
            elif p.name == '4':
                url = getadd4(addr)
            elif p.name == '5':
                url = getadd5(addr)
            elif p.name == '7':
                url = getadd7(addr)
            elif p.name == '10':
                url = getadd10(addr)
            else:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--headless')  # 无界面
                chrome_options.add_argument("--incognito")
                chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在报错问题
                chrome_options.add_argument('--disable-gpu')  # 禁用GPU硬件加速。如果软件渲染器没有就位，则GPU进程将不会启动。
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
                chrome_options.add_argument(
                    'User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36')
                prefs = {"profile.managed_default_content_settings.images": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                # 核心代码
                chrome_options.add_experimental_option('w3c', False)
                caps = DesiredCapabilities.CHROME
                caps['loggingPrefs'] = {'performance': 'ALL'}
                # 核心代码结束
                driver = webdriver.Chrome('D:/software/phantomjs/bin/chromedriver.exe', desired_capabilities=caps,
                                          options=chrome_options)
                try:
                    print(int(time.time() * 1000 - times))
                    driver.get('https://jx.youyitv.com/pp/?url=' + addr)
                    t = 10
                    find = False
                    while t > 0:
                        time.sleep(0.2)
                        log = driver.get_log('performance')
                        for li in (s for s in log if ".m3u8" in s['message']):
                            print(int(time.time() * 1000 - times)*100)
                            message_obj = json.loads(li['message'])
                            if 'request' in message_obj['message']['params']:
                                url = message_obj['message']['params']['request']['url']
                                find = True
                                break
                        if find:
                            break
                        t -= 1
                except:
                    print(traceback.format_exc())
                finally:
                    print(int(time.time() * 1000 - times))
                    driver.quit()
                    print(int(time.time() * 1000 - times))
            if len(url) > 0:
                data_vip_video_url.update_ping(connection, p.id, int(time.time() * 1000 - times))
            else:
                data_vip_video_url.update_ping(connection, p.id, 200000)
    except:
        print(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
