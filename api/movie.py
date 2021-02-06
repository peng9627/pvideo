import json
import traceback

import pymysql
import requests
from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_movie, data_recommend_movie, data_vip, data_agent
from utils import movie_get_rel_addr, project_utils

logger = LoggerUtils('api.movie').logger


def query_movie():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        where = ''
        wheres = []
        if "type" in data:
            move_type = data["type"]
            if len(move_type) < 2:
                wheres.append("type = %s" % move_type)
        if "child_type" in data:
            child_type = data["child_type"]
            if len(child_type) < 4:
                wheres.append("child_type LIKE '%" + child_type + "%'")
        if "region" in data:
            region = data["region"]
            if len(region) < 4:
                wheres.append("region LIKE '%s'" % region)
        if "year" in data:
            year = data["year"]
            if len(year) < 5:
                wheres.append("year LIKE '" + year + "%'")
        if len(wheres) > 0:
            where = "WHERE " + " AND ".join(wheres)
        page = int(data["page"])
        connection = mysql_connection.get_conn()
        videos = data_movie.query_movie_list(connection, where, "ORDER BY update_time DESC", page)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def recommend():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        recommends = data_recommend_movie.query(connection)
        index_recommends = []
        for r in recommends:
            ids = r.ids.split(",")
            where = "WHERE id in (%s)" % ', '.join(ids)
            # where = where % ids
            videos = data_movie.query_movie_list(connection, where, "ORDER BY play_count DESC", 1)
            index_recommend = '{"desc": "%s", "data": [%s]}' % (r.desc, ",".join(videos))
            index_recommends.append(index_recommend)
        result = '{"state":0, "data":[%s]}' % ",".join(index_recommends)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def more():
    result = '{"state":-1}'
    connection = None
    try:
        connection = mysql_connection.get_conn()
        videos = data_movie.query_movie_list(connection, '', "ORDER BY play_count DESC", 1, 6)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def search():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        content = data["content"]
        page = int(data["page"])
        connection = mysql_connection.get_conn()
        videos = data_movie.search(connection, pymysql.converters.escape_string(content), page)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def ranking():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        movie_type = int(data["type"])
        page = int(data["page"])
        connection = mysql_connection.get_conn()
        videos = data_movie.ranking(connection, movie_type, page)
        result = '{"state":0, "data":[%s]}' % ",".join(videos)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def query_info():
    result = '{"state":-1}'
    connection = None
    data = request.form
    try:
        movie_id = data["movie_id"]
        connection = mysql_connection.get_conn()
        movie = data_movie.info(connection, movie_id)
        if movie is not None:
            result = '{"state":0, "data":%s}' % json.dumps(movie.__dict__)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    return result


def get_play_addr():
    result = '{"state":-1}'
    data = request.form
    check_time = 1
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        connection = None
        try:
            connection = mysql_connection.get_conn()
            if not data_vip.is_vip(connection, account_id):
                surplus_time = data_agent.query_min(connection, account_id)
                if surplus_time > 0:
                    data_agent.use_min(connection, account_id, 1)
                    check_time = 0
        except:
            logger.exception(traceback.format_exc())
        finally:
            if connection is not None:
                connection.close()
    elif 1 == code:
        if "HTTP_DEVICE" in request.headers.environ:
            device = request.headers.environ['HTTP_DEVICE']
            redis = gl.get_v("redis")
            if redis.exists("device_info_" + device):
                device_info = redis.getobj("device_info_" + device)
            else:
                device_info = {}
                device_info["surplus_time"] = int(config.get("server", "default_min"))
            if device_info["surplus_time"] > 0:
                device_info["surplus_time"] -= 1
                check_time = 0
                redis.setobj("device_info_" + device, device_info)
        else:
            check_time = 1
    else:
        check_time = 2
    if 0 == check_time:
        url = movie_get_rel_addr.getadds(data['addr'])
        if len(url) > 0:
            return '{"state":0,"data":"%s"}' % url
    else:
        return '{"state":%d}' % check_time
    return result


def play():
    result = '{"state":-1}'
    data = request.args
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        url = movie_get_rel_addr.getadds(data['addr'])
        if len(url) > 0:
            header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            }
            response = requests.get(url, headers=header)
            return response.text, response.status_code, dict(response.headers)
    else:
        result = '{"state":%d}' % code
    return result
