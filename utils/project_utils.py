import json

from pycore.data.entity import globalvar as gl

from pycore.utils import aes_utils
from pycore.utils.stringutils import StringUtils


def get_auth(environ):
    if "HTTP_AUTH" in environ:
        sessionid = environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        if not redis.exists(sessionid):
            return 2, ''
        else:
            sessions = redis.getobj(sessionid)
            return 0, sessions
    else:
        return 1, ''


def flush_auth(environ, sessions):
    if "HTTP_AUTH" in environ:
        sessionid = environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        redis.delobj(sessionid)
        sessionid = 'session' + StringUtils.randomStr(32)
        while redis.exists(sessionid):
            sessionid = 'session' + StringUtils.randomStr(32)
        redis.setexo(sessionid, sessions, 604800)
        return sessionid


def get_key(environ):
    if "HTTP_DEVICE" in environ:
        device = environ['HTTP_DEVICE']
        redis = gl.get_v("redis")
        if redis.exists("device_info_" + device):
            device_info = redis.getobj("device_info_" + device)
            return device_info['aes_key']


def get_data(key, data):
    data = aes_utils.aes_decode(data, key)
    return json.loads(data)


def get_rel_url(url, source):
    if source == 'sw':
        return url[3:]
    else:
        url1 = url.split('#')[0].split('$')[1]
        return url1
