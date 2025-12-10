import json

from pycore.utils import http_utils

page = 1
while page < 21:
    s = http_utils.HttpUtils("cjhwba.com").get_with_ssl(
        "/api.php/provide/vod/?ac=detail&pg=%d&pagesize=100" % page, None)
    data = json.loads(s)
    if len(data) == 0:
        break
    else:
        out = open('./conf/movie_jsons/hw8/movie-%d.json' % page, 'w')
        out.write(json.dumps(data))
        out.close()
    page += 1
