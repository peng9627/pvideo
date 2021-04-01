import json
import random
import time
import traceback

import pymysql
import requests
from flask import request
from pycore.data.database import mysql_connection
from pycore.data.entity import config, globalvar as gl
from pycore.utils import aes_utils, time_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_movie, data_recommend_movie, data_vip, data_agent, data_video_history, data_play_details
from utils import movie_get_rel_addr, project_utils

logger = LoggerUtils('api.movie').logger


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
                        wheres.append("region LIKE '%" + region + "%'")
                if "year" in data:
                    year = data["year"]
                    if len(year) < 5:
                        wheres.append("year LIKE '" + year + "%'")
                if len(wheres) > 0:
                    where = "WHERE " + " AND ".join(wheres)
                page = int(data["page"])
                connection = mysql_connection.get_conn()
                videos = data_movie.query(connection, where, "ORDER BY year DESC, update_time DESC", page)
                result = '{"state":0, "data":[%s]}' % ",".join(videos)
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
            videos = data_movie.query(connection, '', "ORDER BY play_count DESC", 1, 9)
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
                connection = mysql_connection.get_conn()
                videos = data_movie.search(connection, pymysql.converters.escape_string(content), page)
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
                movie.play_count *= 30
                movie.play_count += random.randint(1, 30)
                if movie is not None:
                    code, sessions = project_utils.get_auth(request.headers.environ)
                    content = ''
                    if 0 == code:
                        account_id = sessions["id"]
                        content = data_video_history.content(connection, account_id, movie_id)
                    result = '{"state":0, "data":%s,"content":"%s"}' % (json.dumps(movie.__dict__), content)
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()
        return aes_utils.aes_encode(result, key)
    return result


def get_play_addr():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        address = None
        if data is not None:
            redis = gl.get_v("redis")
            check_time = 1
            not_line = []
            device_info = {}
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                if data['switch'] and 'current_line' in sessions:
                    if 'not_line' in sessions:
                        not_line = sessions['not_line']
                    not_line.append(sessions['current_line'])
                    address = sessions['current_address']
                    check_time = 0
                else:
                    address = data['addr']
                    connection = None
                    try:
                        connection = mysql_connection.get_conn()
                        if not data_vip.is_vip(connection, account_id):
                            surplus_time = data_agent.query_times(connection, account_id)
                            if surplus_time > 0:
                                data_agent.use_times(connection, account_id, 1)
                                check_time = 0
                        else:
                            check_time = 0
                    except:
                        logger.exception(traceback.format_exc())
                    finally:
                        if connection is not None:
                            connection.close()
            elif 1 == code:
                if "HTTP_DEVICE" in request.headers.environ:
                    device = request.headers.environ['HTTP_DEVICE']
                    if redis.exists("device_info_" + device):
                        device_info = redis.getobj("device_info_" + device)
                    else:
                        device_info = {}
                        device_info["surplus_time"] = int(config.get("server", "default_times"))
                    if data['switch'] and 'current_line' in device_info:
                        if 'not_line' in device_info:
                            not_line = device_info['not_line']
                        not_line.append(device_info['current_line'])
                        address = device_info['current_address']
                        check_time = 0
                    elif device_info["surplus_time"] > 0:
                        device_info["surplus_time"] -= 1
                        check_time = 0
                        address = data['addr']
                else:
                    check_time = 1
            else:
                check_time = 2
            if 0 == check_time:
                url, name = movie_get_rel_addr.getadds(address, not_line)
                if len(url) == 0:
                    not_line.clear()
                    url, name = movie_get_rel_addr.getadds(address, [])
                if len(url) > 0:
                    if 0 == code:
                        sessions['current_line'] = name
                        sessions['not_line'] = not_line
                        sessions['current_address'] = address
                        redis.setexo(request.headers.environ['HTTP_AUTH'], sessions, 604800)
                    else:
                        device_info['current_line'] = name
                        device_info['not_line'] = not_line
                        device_info['current_address'] = address
                        redis.setobj("device_info_" + request.headers.environ['HTTP_DEVICE'], device_info)
                    result = '{"state":0,"data":"%s"}' % url
            else:
                result = '{"state":%d}' % check_time
        return aes_utils.aes_encode(result, key)
    return result


def play():
    result = '{"state":-1}'
    data = request.args
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        url = movie_get_rel_addr.getadds(data['addr'], [])
        if len(url) > 0:
            header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
            }
            response = requests.get(url, headers=header)
            return response.text, response.status_code, dict(response.headers)
    else:
        result = '{"state":%d}' % code
    return result
