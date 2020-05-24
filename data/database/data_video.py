# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.video import Video

logger = LoggerUtils("data_video").logger


def create_video(connection, video):
    try:
        sql = config.get("sql", "sql_add_video")
        with connection.cursor() as cursor:
            cursor.execute(sql, (
                video.type, video.title, video.create_time, video.address, video.horizontal, video.vertical))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def query_video_list(connection, type, page, pagesize=20):
    video_list = []
    try:
        with connection.cursor() as cursor:
            if -1 == type:
                sql = config.get("sql", "sql_video_count")
                cursor.execute(sql, ((page - 1) * pagesize, pagesize))
            elif 0 == type:
                sql = config.get("sql", "sql_video_newest")
                cursor.execute(sql, ((page - 1) * pagesize, pagesize))
            else:
                sql = config.get("sql", "sql_video_list")
                cursor.execute(sql, (type, (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                v = Video()
                v.id = result["id"]
                v.title = result["title"]
                v.create_time = result["create_time"]
                v.play_count = result["play_count"]
                v.address = result["address"]
                v.horizontal = result["horizontal"]
                v.vertical = result["vertical"]
                video_list.append(json.dumps(v.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return video_list


def query_video_search(connection, content, page, pagesize=20):
    video_list = []
    try:
        sql = config.get("sql", "sql_video_search")
        with connection.cursor() as cursor:
            cursor.execute(sql, ("%" + content + "%", (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                v = Video()
                v.id = result["id"]
                v.title = result["title"]
                v.create_time = result["create_time"]
                v.play_count = result["play_count"]
                v.address = result["address"]
                v.horizontal = result["horizontal"]
                v.vertical = result["vertical"]
                video_list.append(json.dumps(v.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return video_list


def query_video_by_ids(connection, ids):
    video_list = []
    try:
        in_p = ', '.join((map(lambda x: '%s', ids)))
        sql = config.get("sql", "sql_query_video_by_ids") % in_p
        with connection.cursor() as cursor:
            cursor.execute(sql, ids)
            r = cursor.fetchall()
            for result in r:
                v = Video()
                v.id = result["id"]
                v.title = result["title"]
                v.create_time = result["create_time"]
                v.play_count = result["play_count"]
                v.address = result["address"]
                v.horizontal = result["horizontal"]
                v.vertical = result["vertical"]
                video_list.append(v)
    except:
        logger.exception(traceback.format_exc())
    return video_list


def video_add_count(connection, id):
    try:
        sql = config.get("sql", "sql_video_add_count")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())
