# -*- coding: utf-8 -*-
import requests
import json, sys
import random

from utils.douyu import main

reload(sys)
sys.setdefaultencoding("utf-8")

Max = 2  # 斗鱼页数


def createRandomString(len):
    print ('wet'.center(10, '*'))
    raw = ""
    range1 = range(58, 65)  # between 0~9 and A~Z
    range2 = range(91, 97)  # between A~Z and a~z

    i = 0
    while i < len:
        seed = random.randint(48, 122)
        if ((seed in range1) or (seed in range2)):
            continue
        raw += chr(seed)
        i += 1
    return raw


def getNumber():
    p = 0
    urls = ['https://m.douyu.com/api/room/list?page={}&type=LOL'.format(page) for page in range(1, Max)]
    fp = open("/Users/pengyi/douyu_" + createRandomString(4) + ".txt", "w")
    fp.write("「斗鱼」\n")
    for url in urls:
        res = requests.get(url)
        j = json.loads(res.text)
        l1 = j['data']
        l2 = l1['list']
        p = p + 1
        fp.write("==第%d页==\n" % p)
        for i in range(len(l2)):
            Anchor = l2[i]['nickname']
            RoomNumber = l2[i]['rid']
            # print Anchor + u"," + main(RoomNumber) + u"\n"
            if not u"未开播" in main(RoomNumber):
                fp.write(Anchor + u"," + main(RoomNumber) + u"\n")

    fp.write("\n")
    fp.close()
    print(u'斗鱼房间数据已保存')


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    getNumber()
