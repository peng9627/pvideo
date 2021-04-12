import time
import traceback

import requests
from pycore.data.database import mysql_connection
from pycore.data.entity import config

from data.database import data_vip_video_url, data_video_real_addr


def get_addr(addr, not_line):
    connection = None
    try:
        connection = mysql_connection.get_conn()
        cache_addrs = data_video_real_addr.query(connection, addr)
        parse_urls = data_vip_video_url.query(connection)
        # 循环所有线路
        for p in parse_urls:
            # 切换掉的线路不要
            if p.id in not_line:
                continue
            else:
                # 优先从缓存里面找
                for cache_addr in cache_addrs:
                    if cache_addr['url_id'] == p.id:
                        url = cache_addr['rel_address']
                        return url, p.id
        # 所有线路都没有缓存 调用解析 不要的线路优先去掉 除非没找到
        data = {'addr': addr, 'not_line': ','.join('%s' % url_id for url_id in not_line)}
        # data = {'addr': addr, 'not_line': not_line}
        result = requests.post(config.get("server", "vip_parse_url"), data, timeout=45).json()
        url = result['url']
        url_id = result['url_id']
        if len(url) > 0:
            # 存入缓存
            data_video_real_addr.add(connection, int(time.time()), url_id, addr, url)
            return url, url_id
    except:
        print(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return '', 0
