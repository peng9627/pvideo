# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.video import Video

logger = LoggerUtils("data.video").logger


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
            if -2 == type:
                sql = config.get("sql", "sql_video_count")
                cursor.execute(sql, ((page - 1) * pagesize, pagesize))
            elif -1 == type:
                sql = config.get("sql", "sql_video_newest")
                cursor.execute(sql, ((page - 1) * pagesize, pagesize))
            else:
                sql = config.get("sql", "sql_video_list")
                cursor.execute(sql, (type, (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                v = Video()
                v.id = result["id"]
                v.type = result["type"]
                v.title = result["title"]
                v.create_time = result["create_time"]
                v.play_count = result["play_count"]
                address = result["address"]
                if address.find('://') >= 0:
                    v.address = address
                else:
                    v.address = config.get("server", "video_video_domain") + address
                horizontal = result["horizontal"]
                if horizontal.find('://') >= 0:
                    v.horizontal = horizontal
                else:
                    v.horizontal = config.get("server", "video_img_domain") + horizontal
                vertical = result["vertical"]
                if vertical.find('://') >= 0:
                    v.vertical = vertical
                else:
                    v.vertical = config.get("server", "video_img_domain") + vertical
                video_list.append(json.dumps(v.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return video_list


def recommend(connection):
    video_list = []
    try:
        with connection.cursor() as cursor:
            sql = config.get("sql", "sql_video_recommend")
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                v = Video()
                v.id = result["id"]
                v.type = result["type"]
                v.title = result["title"]
                v.create_time = result["create_time"]
                v.play_count = result["play_count"]
                address = result["address"]
                if address.find('://') >= 0:
                    v.address = address
                else:
                    v.address = config.get("server", "video_video_domain") + address
                horizontal = result["horizontal"]
                if horizontal.find('://') >= 0:
                    v.horizontal = horizontal
                else:
                    v.horizontal = config.get("server", "video_img_domain") + horizontal
                vertical = result["vertical"]
                if vertical.find('://') >= 0:
                    v.vertical = vertical
                else:
                    v.vertical = config.get("server", "video_img_domain") + vertical
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
                v.type = result["type"]
                v.title = result["title"]
                v.create_time = result["create_time"]
                v.play_count = result["play_count"]
                address = result["address"]
                if address.find('://') >= 0:
                    v.address = address
                else:
                    v.address = config.get("server", "video_video_domain") + address
                horizontal = result["horizontal"]
                if horizontal.find('://') >= 0:
                    v.horizontal = horizontal
                else:
                    v.horizontal = config.get("server", "video_img_domain") + horizontal
                vertical = result["vertical"]
                if vertical.find('://') >= 0:
                    v.vertical = vertical
                else:
                    v.vertical = config.get("server", "video_img_domain") + vertical
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
                v.type = result["type"]
                v.title = result["title"]
                v.create_time = result["create_time"]
                v.play_count = result["play_count"]
                address = result["address"]
                if address.find('://') >= 0:
                    v.address = address
                else:
                    v.address = config.get("server", "video_video_domain") + address
                horizontal = result["horizontal"]
                if horizontal.find('://') >= 0:
                    v.horizontal = horizontal
                else:
                    v.horizontal = config.get("server", "video_img_domain") + horizontal
                vertical = result["vertical"]
                if vertical.find('://') >= 0:
                    v.vertical = vertical
                else:
                    v.vertical = config.get("server", "video_img_domain") + vertical
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


def info(connection, video_id):
    video_info = {}
    try:
        sql = config.get("sql", "sql_video_info")
        with connection.cursor() as cursor:
            cursor.execute(sql, video_id)
            result = cursor.fetchone()
            if result is not None:
                video_info["type"] = result["type"]
                video_info["title"] = result["title"]
                video_info["create_time"] = result["create_time"]
                video_info["play_count"] = result["play_count"]
    except:
        logger.exception(traceback.format_exc())
    return video_info
#
# def video_add_comment(connection, id):
#     try:
#         sql = config.get("sql", "sql_video_add_comment")
#         with connection.cursor() as cursor:
#             cursor.execute(sql, id)
#             connection.commit()
#     except:
#         connection.rollback()
#         logger.exception(traceback.format_exc())
#
#
# def video_add_praise(connection, id):
#     try:
#         sql = config.get("sql", "sql_video_add_praise")
#         with connection.cursor() as cursor:
#             cursor.execute(sql, id)
#             connection.commit()
#     except:
#         connection.rollback()
#         logger.exception(traceback.format_exc())
#
#
# def video_cancel_praise(connection, id):
#     try:
#         sql = config.get("sql", "sql_video_cancel_praise")
#         with connection.cursor() as cursor:
#             cursor.execute(sql, id)
#             connection.commit()
#     except:
#         connection.rollback()
#         logger.exception(traceback.format_exc())
#
