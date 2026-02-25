import json
import re
import time
import traceback

import pymysql
import requests
from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import config
from pycore.utils import aes_utils, time_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_movie, data_recommend_movie, data_vip, data_video_history, data_play_details, \
    data_video_praise, data_video_comment
from utils import project_utils
from utils.project_utils import get_rel_url

logger = LoggerUtils('api.movie').logger

recommends = ['电影', '电视剧', '短剧', '动漫', '综艺', '体育', '纪录片']
types = [20, 60, 120, 80, 82, 84, 86]
recommendsKey = ['movie', 'tv_drama', 'short_drama', 'cartoon', 'variety_show', 'physical_education',
                 'documentary']


def query():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                where = ''
                wheres = []
                if "span" in data:
                    move_span = data["span"]
                    if move_span in recommendsKey:
                        idx = recommendsKey.index(move_span)
                        wheres.append("type = %d" % types[idx])
                    elif len(move_span) > 0:
                        wheres.append("span LIKE '%" + move_span + "%'")
                if "type" in data:
                    move_type = data["type"]
                    if len(move_type) < 2:
                        wheres.append("type = %s" % move_type)
                else:
                    wheres.append("type != 0")
                if "child_type" in data:
                    child_type = data["child_type"]
                    if len(child_type) < 4:
                        wheres.append("child_type LIKE '%" + child_type + "%'")
                if "region" in data:
                    region = data["region"]
                    if len(region) < 4:
                        wheres.append("region LIKE '%" + region + "%'")
                if "year" in data:
                    year = data["year"]
                    if len(year) < 5:
                        wheres.append("year LIKE '%" + year + "%'")
                if "content" in data:
                    content = data["content"]
                    c = pymysql.converters.escape_string(content)
                    wheres.append("(title LIKE '%" + c + "%' OR span LIKE '%" + c + "%' OR child_type LIKE '%" + c + "%')")
                if len(wheres) > 0:
                    where = "WHERE " + " AND ".join(wheres)
                page = int(data["page"])
                page_size = 12
                if 'count' in data:
                    page_size = int(data["count"])
                connection = mysql_connection.get_conn()
                videos = data_movie.query(connection, where, "ORDER BY update_time DESC", page, page_size)
                result = '{"state":0, "data":[%s]}' % ",".join(videos)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def query_short():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                connection = mysql_connection.get_conn()
                videos = data_movie.query_short(connection)
                result = '{"state":0, "data":[%s]}' % ",".join(videos)
                #
                #
                # code, sessions = project_utils.get_auth(request.headers.environ)
                # result = '{"state":3}'
                # if 0 == code:
                #     connection = mysql_connection.get_conn()
                #     account_id = sessions["id"]
                #     if data_vip.is_vip(connection, account_id):
                #         videos = data_movie.query_short(connection)
                #         result = '{"state":0, "data":[%s]}' % ",".join(videos)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def index():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                count = int(data['count'])
                connection = mysql_connection.get_conn()
                index_recommends = []
                videos = data_movie.query(connection, '', "ORDER BY update_time DESC", 1, count)
                index_recommend = '{"desc": "%s", "data": [%s]}' % ('last_updated', ",".join(videos))
                index_recommends.append(index_recommend)
                videos = data_movie.query(connection, '', "ORDER BY play_count DESC", 1, count)
                index_recommend = '{"desc": "%s", "data": [%s]}' % ('most_popular', ",".join(videos))
                index_recommends.append(index_recommend)
                for i in range(0, len(recommends)):
                    where = "WHERE span LIKE '%" + recommends[i] + "%' OR title LIKE '%" + recommends[
                        i] + "%' OR child_type LIKE '%" + recommends[i] + "%' "
                    videos = data_movie.query(connection, where, "ORDER BY update_time DESC", 1, count)
                    index_recommend = '{"desc": "%s", "data": [%s]}' % (recommendsKey[i], ",".join(videos))
                    index_recommends.append(index_recommend)
                result = '{"state":0, "data":[%s]}' % ",".join(index_recommends)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def recommend():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        connection = None
        try:
            connection = mysql_connection.get_conn()
            recommends = data_recommend_movie.query(connection)
            index_recommends = []
            for r in recommends:
                ids = r.ids.split(",")
                where = "WHERE id in (%s)" % ', '.join(ids)
                # where = where % ids
                videos = data_movie.query(connection, where, "ORDER BY play_count DESC", 1)
                index_recommend = '{"desc": "%s", "data": [%s]}' % (r.desc, ",".join(videos))
                index_recommends.append(index_recommend)
            result = '{"state":0, "data":[%s]}' % ",".join(index_recommends)
        except:
            logger.exception(traceback.format_exc())
        finally:
            if connection is not None:
                connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def more():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        connection = None
        try:
            connection = mysql_connection.get_conn()
            videos = data_movie.query(connection, '', "ORDER BY play_count DESC", 1, 8)
            result = '{"state":0, "data":[%s]}' % ",".join(videos)
        except:
            logger.exception(traceback.format_exc())
        finally:
            if connection is not None:
                connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def search():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                content = data["content"]
                page = int(data["page"])
                page_size = 12
                if 'count' in data:
                    page_size = int(data["count"])
                connection = mysql_connection.get_conn()
                videos = data_movie.search(connection, pymysql.converters.escape_string(content), page, page_size)
                result = '{"state":0, "data":[%s]}' % ",".join(videos)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def ranking():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                movie_type = int(data["type"])
                page = int(data["page"])
                days = int(data["days"])
                t = time.time()
                time_string = time_utils.stamp_to_string(t, '%Y/%m/%d')
                time_stamp = time_utils.string_to_stamp(time_string, '%Y/%m/%d') - 1 - days * 86400
                connection = mysql_connection.get_conn()
                videos = data_movie.ranking(connection, time_stamp, movie_type, page)
                result = '{"state":0, "data":[%s]}' % ",".join(videos)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def query_details():
    result = '{"state":-1}'
    connection = None
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            try:
                video_id = data["video_id"]
                connection = mysql_connection.get_conn()
                praises = data_video_praise.count(connection, '%,' + str(video_id))
                comments = data_video_comment.count(connection, video_id)
                praised = False
                code, sessions = project_utils.get_auth(request.headers.environ)
                if 0 == code:
                    account_id = sessions["id"]
                    praised = data_video_praise.exist(connection, str(account_id) + "," + str(video_id))
                result = '{"state":0, "data":{"praises":%d, "comments":%d, "praised":%d}}' % (
                    praises, comments, 1 if praised else 0)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def query_info():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            connection = None
            try:
                movie_id = data["movie_id"]
                connection = mysql_connection.get_conn()
                data_movie.add_count(connection, movie_id)
                t = time.time()
                time_string = time_utils.stamp_to_string(t, '%Y/%m/%d')
                time_stamp = time_utils.string_to_stamp(time_string, '%Y/%m/%d')
                data_play_details.create(connection, movie_id, time_stamp)
                movie = data_movie.info(connection, movie_id)
                movie.is_vip = False
                if movie is not None:
                    code, sessions = project_utils.get_auth(request.headers.environ)
                    content = ''
                    movie.is_vip = False
                    # movie.address= "http://playertest.longtailvideo.com/adaptive/bipbop/gear4/prog_index.m3u8?a=1&n=2"
                    movie.address = config.get("server", "server_url") + "/play_movie/" + movie_id
                    if 0 == code:
                        account_id = sessions["id"]
                        content = data_video_history.content(connection, account_id, movie_id)
                        if data_vip.is_vip(connection, account_id):
                            movie.is_vip = True
                    result = '{"state":0, "data":%s,"content":"%s"}' % (json.dumps(movie.__dict__), content)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def play(movie_id):
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    is_vip = False
    url = None
    source = None
    connection = None
    try:
        connection = mysql_connection.get_conn()
        url, source = data_movie.get_url(connection, movie_id)
        if 0 == code:
            account_id = sessions["id"]
            if data_vip.is_vip(connection, account_id):
                is_vip = True
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    if url is None:
        return "error"
    rel_url = get_rel_url(url.strip(), source)
    infile = requests.get(rel_url).text
    if is_vip:
        text = infile
    else:
        parts = infile.count('\n')
        if parts > 100:
            matches = [m.start() for m in re.finditer('\n', infile)]
            if len(matches) > 100:
                start1 = matches[100]
                start2 = infile.find("#EXTINF:", start1)
                text = infile[0:start2]
                text += "#EXT-X-ENDLIST\n"

        # parts = infile.count('#EXTINF:')
        # if parts > 2:
        #     start1 = infile.find("#EXTINF:", 0)
        #     start2 = infile.find("#EXTINF:", start1 + 1)
        #     start3 = infile.find("#EXTINF:", start2 + 1)
        #     text = infile[0:start3]
        #     text += "#EXT-X-ENDLIST\n"
        else:
            text = infile
    lines = text.splitlines(True)
    url_end_index = len(rel_url) - list(reversed(rel_url)).index('/')
    rel_content = ''
    for line in lines:
        if '.ts' in line:
            rel_content += rel_url[:url_end_index] + line
        else:
            rel_content += line
    if rel_content is not None:
        print(rel_content)
        return rel_content, 200, {"Accept-Ranges": 'bytes',
                                  "Content-Type": "application/vnd.apple.mpegurl; charset=utf-8"}
    return result
