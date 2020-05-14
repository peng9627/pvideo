# coding=utf-8
import httplib
import json
import traceback

from flask import request
from pycore.utils.logger_utils import LoggerUtils

from utils.douyu import get_real_url

logger = LoggerUtils('api.game').logger

reqheaders = {'Content-type': 'application/x-www-form-urlencoded',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Host': 'm.douyu.com',
              'scheme': 'https',
              'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1', }


def games():
    result = '{"state":-1}'

    try:
        datas = []
        try:
            infile = open('/Users/pengyi/PycharmProjects/h5video/conf/douyu_type.json')
            videos = json.load(infile)
            infile.close()
            for g in videos:
                datas.append(json.dumps({"id": g["shortName"], "name": g["cate2Name"], "pic": g["icon"]}))
            result = '{"state":0, "data":[%s]}' % ",".join(datas)
        except:
            logger.exception(traceback.format_exc())

    except:
        logger.exception(traceback.format_exc())
    return result


def lives():
    result = '{"state":-1}'

    try:
        datas = []
        data = request.form
        try:
            id = data["id"]
            page = data["page"]
            conn = httplib.HTTPSConnection('m.douyu.com')
            conn.request("GET", "/api/room/list?page=%s&type=%s" % (page, id), headers=reqheaders)
            res = conn.getresponse().read()
            for g in json.loads(res)["data"]["list"]:
                RoomNumber = g['rid']
                datas.append(
                    json.dumps({"video": get_real_url(RoomNumber), "name": g["roomName"], "pic": g["roomSrc"],
                                "nick": g["nickname"]}))
            result = '{"state":0, "data":[%s]}' % ",".join(datas)
        except:
            logger.exception(traceback.format_exc())

    except:
        logger.exception(traceback.format_exc())
    return result
