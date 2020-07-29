# coding=utf-8
import json
import traceback

from pycore.utils.http_utils import HttpUtils
from pyquery import PyQuery

from mode.movie import Movie

if __name__ == '__main__':
    page = 137
    while page > 0:
        # s = HttpUtils("hao123.daicuo.cc").get("/channel/2-%d.html" % page, None)
        s = HttpUtils("hao123.daicuo.cc").get("/channel/4-%d.html" % page, None)
        if s is not None and len(s) > 0:
            d = PyQuery(s)
            videos = d('tbody:first').children("tr")
            movies = []
            for v in videos.items():
                infos = v("td")

                href = PyQuery(infos[0])("a:first").attr("href")
                ss = HttpUtils("hao123.daicuo.cc").get(href, None)
                if ss is not None and len(ss) > 0:
                    try:
                        movie = Movie()
                        movie.title = PyQuery(infos[0])("a:first").attr("title")
                        movie.span = PyQuery(infos[0]).text().replace(movie.title, '').strip()
                        movie.type = PyQuery(infos[1])("a:first").text()
                        movie.update_time = PyQuery(infos[2]).text()

                        de = PyQuery(ss)
                        movie.vertical = de("div").filter(".media-left")("a:first")("img:first").attr("data-original")
                        video_details = de("div").filter(".media-body")("dl").children()
                        for i in range(0, len(video_details) - 1, 2):
                            ss = PyQuery(video_details[i]).text()
                            if u'主演：' == ss:
                                actors = []
                                for a in PyQuery(video_details[i + 1])("a").items():
                                    actors.append(a.text())
                                movie.actor = ",".join(actors)
                            elif u"子类：" == ss:
                                child_type = []
                                for a in PyQuery(video_details[i + 1])("a").items():
                                    child_type.append(a.text())
                                movie.child_type = ",".join(child_type)
                            elif u"导演：" == ss:
                                director = []
                                for a in PyQuery(video_details[i + 1])("a").items():
                                    director.append(a.text())
                                movie.director = ",".join(director)
                            elif u"地区：" == ss:
                                region = []
                                for a in PyQuery(video_details[i + 1])("a").items():
                                    region.append(a.text())
                                movie.region = ",".join(region)
                            elif u"年份：" == ss:
                                year = []
                                for a in PyQuery(video_details[i + 1])("a").items():
                                    year.append(a.text())
                                movie.year = ",".join(year)
                            elif u"总集：" == ss:
                                movie.total_part = PyQuery(video_details[i + 1]).text()
                            elif u"剧情：" == ss:
                                movie.details = PyQuery(video_details[i + 1])("span:last").text()
                            elif u"类型：" != ss:
                                print ss.encode("utf-8")
                        # if len(video_details) < 8:
                        #     # if len(video_details) < 7:
                        #     continue
                        # actors = []
                        # for a in PyQuery(video_details[0])("a").items():
                        #     actors.append(a.text())
                        # movie.actor = ",".join(actors)
                        # child_type = []
                        # for a in PyQuery(video_details[2])("a").items():
                        #     child_type.append(a.text())
                        # movie.child_type = ",".join(child_type)
                        # director = []
                        # for a in PyQuery(video_details[3])("a").items():
                        #     director.append(a.text())
                        # movie.director = ",".join(director)
                        # region = []
                        # for a in PyQuery(video_details[4])("a").items():
                        #     region.append(a.text())
                        # movie.region = ",".join(region)
                        # year = []
                        # for a in PyQuery(video_details[5])("a").items():
                        #     year.append(a.text())
                        # movie.year = ",".join(year)
                        # movie.total_part = PyQuery(video_details[6]).text()
                        # movie.details = PyQuery(video_details[7])("span:last").text()
                        # movie.details = PyQuery(video_details[6])("span:last").text()

                        playurl = de("dl").filter(".vod-item-playurl")
                        movie.source = playurl("dt:first")("span").filter(".text-primary").text()
                        parts = playurl("dd")
                        if len(parts) == 0:
                            continue
                        address = []
                        for a in parts.items():
                            if a("a:first").text() not in address:
                                address.append(a("a:first").text())
                        movie.address = ",".join(address)
                        movies.append(movie.__dict__)
                    except:
                        print traceback.format_exc()
            out = open('./conf/movie_jsons/movie-4-%d.json' % page, 'w')
            out.write(json.dumps(movies))
            out.close()
        page -= 1
