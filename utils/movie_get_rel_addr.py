import base64
import json
import os
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


def getadd13(addr):
    vdjs = ''
    try:
        result = requests.get('https://www.administratorm.com/WANG/index.php?url=' + parse.quote(addr), headers=headers,
                              timeout=10).text
        vdjss = result.find('vkey=\'') + 6
        vdjse = result.find('\'', vdjss)
        vkey = result[vdjss:vdjse]
        datas = {'url': addr, 'wap': '0', 'ios': '0', 'vkey': vkey, 'type': ''}
        result = requests.post('https://www.administratorm.com/WANG/Api.php', headers=headers, data=datas,
                               timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd14(addr):
    vdjs = ''
    try:
        datas = {'url': addr, 'referer': '', 'ref': '0', 'time': '1611645821', 'type': '',
                 'other': str(base64.b64encode(addr.encode("utf-8"))), 'ios': ''}
        result = requests.post('https://www.administratorm.com/api.php', headers=headers, data=datas, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd15(addr):
    vdjs = ''
    try:
        datas = {'url': addr, 'referer': '', 'ref': '0', 'time': '1611645821', 'type': '',
                 'other': str(base64.b64encode(addr.encode("utf-8"))), 'ios': ''}
        result = requests.post('http://m3u8.boquxinxi.com/jiexi/api.php', headers=headers, data=datas, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd16(addr):
    vdjs = ''
    try:
        datas = {'url': addr, 'referer': '', 'ref': '0', 'time': '1611645821', 'type': '',
                 'other': str(base64.b64encode(addr.encode("utf-8"))), 'ios': ''}
        result = requests.post('https://man.ledboke.com/147/apikey.php', headers=headers, data=datas, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
    except:
        print(traceback.format_exc())
    finally:
        return vdjs


def getadd17(addr):
    vdjs = ''
    try:
        result = requests.get('https://vip.mpos.ren/rends/api.php?url=' + parse.quote(addr) + '&danmu=0',
                              headers=headers, timeout=10).text
        vdjss = result.find('"url":"') + 7
        vdjse = result.find('"', vdjss)
        vdjs = result[vdjss:vdjse].replace("\\", '')
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


def getadds(addr, not_line):
    connection = None
    url = ''
    name = ''
    try:
        connection = mysql_connection.get_conn()
        parse_urls = data_vip_video_url.query(connection)
        for p in parse_urls:
            if p.name in not_line:
                continue
            elif p.name == '2':
                url = getadd2(addr)
            elif p.name == '3':
                url = getadd3(addr)
            elif p.name == '4':
                url = getadd4(addr)
            elif p.name == '5':
                url = getadd5(addr)
            elif p.name == '10':
                url = getadd10(addr)
            elif p.name == '13':
                url = getadd13(addr)
            elif p.name == '14':
                url = getadd14(addr)
            elif p.name == '15':
                url = getadd15(addr)
            elif p.name == '16':
                url = getadd16(addr)
            elif p.name == '17':
                url = getadd17(addr)
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
                driver = None
                try:
                    # 核心代码结束
                    # driver = webdriver.Chrome('D:/software/phantomjs/bin/chromedriver.exe', desired_capabilities=caps,
                    #                           options=chrome_options)
                    driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
                    driver.set_page_load_timeout(8)
                    driver.set_script_timeout(8)
                    driver.get(p.address + addr)
                    t = 20
                    find = False
                    while t > 0:
                        time.sleep(0.2)
                        log = driver.get_log('performance')
                        for li in (s for s in log if ('.m3u8' in s['message'] or '.mp4' in s['message'])):
                            message_obj = json.loads(li['message'])
                            if 'request' in message_obj['message']['params']:
                                url = message_obj['message']['params']['request']['url']
                                if url.endswith(".m3u8") or url.endswith(".mp4") or '.m3u8?' in url or '.mp4?' in url:
                                    find = True
                                    break
                        if find:
                            break
                        t -= 1
                except:
                    print(traceback.format_exc())
                finally:
                    if driver is not None:
                        driver.quit()
                    # os.system('kill -s 9 `pgrep chrome`')
                    # os.system('taskkill /im chromedriver.exe /F')
                    # os.system('taskkill /im chrome.exe /F')
            if len(url) > 0 and (url.endswith(".m3u8") or url.endswith(".mp4") or '.m3u8?' in url or '.mp4?' in url):
                name = p.name
                break
    except:
        print(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return url, name


def check_adds(addr):
    connection = None
    try:
        connection = mysql_connection.get_conn()
        parse_urls = data_vip_video_url.query(connection)
        for p in parse_urls:
            url = ''
            times = time.time() * 1000
            if p.name == '2':
                url = getadd2(addr)
            elif p.name == '3':
                url = getadd3(addr)
            elif p.name == '4':
                url = getadd4(addr)
            elif p.name == '5':
                url = getadd5(addr)
            elif p.name == '10':
                url = getadd10(addr)
            elif p.name == '13':
                url = getadd13(addr)
            elif p.name == '14':
                url = getadd14(addr)
            elif p.name == '15':
                url = getadd15(addr)
            elif p.name == '16':
                url = getadd16(addr)
            elif p.name == '17':
                url = getadd17(addr)
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
                # driver = webdriver.Chrome('D:/software/phantomjs/bin/chromedriver.exe', desired_capabilities=caps,
                #                           options=chrome_options)
                driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
                try:
                    driver.set_page_load_timeout(8)
                    driver.set_script_timeout(8)
                    driver.get(p.address + addr)
                    t = 20
                    find = False
                    while t > 0:
                        time.sleep(0.2)
                        log = driver.get_log('performance')
                        for li in (s for s in log if ('.m3u8' in s['message'] or '.mp4' in s['message'])):
                            message_obj = json.loads(li['message'])
                            if 'request' in message_obj['message']['params']:
                                url = message_obj['message']['params']['request']['url']
                                if url.endswith(".m3u8") or url.endswith(".mp4") or '.m3u8?' in url or '.mp4?' in url:
                                    find = True
                                    break
                        if find:
                            break
                        t -= 1
                except:
                    print(traceback.format_exc())
                finally:
                    driver.quit()
                    # os.system('kill -s 9 `pgrep chrome`')
                    # os.system('taskkill /im chromedriver.exe /F')
                    # os.system('taskkill /im chrome.exe /F')
            if len(url) > 0 and (url.endswith(".m3u8") or url.endswith(".mp4") or '.m3u8?' in url or '.mp4?' in url):
                data_vip_video_url.update_ping(connection, p.id, int(time.time() * 1000 - times))
            else:
                data_vip_video_url.update_ping(connection, p.id, 200000)
    except:
        print(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
