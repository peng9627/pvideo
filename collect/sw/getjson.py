import json

from pycore.utils import http_utils

page = 1
while page < 20:
    s = http_utils.HttpUtils("siwazyw.tv").get_with_ssl(
        "/api.php/provide/vod/at/json/?ac=detail&pg=%d" % page, None)
    data = json.loads(s)
    if len(data) == 0:
        break
    else:
        out = open('./conf/movie_jsons/movie-%d.json' % page, 'w')
        out.write(json.dumps(data))
        out.close()
    page += 1
