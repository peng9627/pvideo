# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.movie import Movie

logger = LoggerUtils("data.movie").logger


def create(connection, movie):
    try:
        if not exist(connection, movie):
            sql = config.get("sql", "sql_add_movie")
            with connection.cursor() as cursor:
                cursor.execute(sql, (
                    movie.type, movie.title, movie.span, movie.create_time, movie.update_time, movie.address,
                    movie.horizontal, movie.vertical, movie.actor, movie.child_type, movie.director, movie.region,
                    movie.year, movie.total_part, movie.details, movie.source))
                connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def query(connection, where, order, page, pagesize=12):
    movie_list = []
    try:
        with connection.cursor() as cursor:
            sql = config.get("sql", "sql_movie_list") % (where, order, (page - 1) * pagesize, pagesize)
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                v = Movie()
                v.id = result["id"]
                v.type = result["type"]
                v.title = result["title"]
                v.span = result["span"]
                v.update_time = result["update_time"]
                v.play_count = result["play_count"]
                v.play_count *= 31
                v.play_count += 1
                v.horizontal = config.get("server", "img_domain") + result["horizontal"]
                v.vertical = config.get("server", "img_domain") + result["vertical"]
                movie_list.append(json.dumps(v.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return movie_list


def query_short(connection):
    movie_list = []
    try:
        with connection.cursor() as cursor:
            sql = config.get("sql", "sql_movie_short")
            cursor.execute(sql, ("%小视频%", 0, 3))
            r = cursor.fetchall()
            for result in r:
                v = Movie()
                v.id = result["id"]
                v.title = result["title"]
                v.address = config.get("server", "server_url") + "/play_movie/" + str(v.id)
                movie_list.append(json.dumps(v.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return movie_list


def search(connection, content, page, pagesize=20):
    movie_list = []
    try:
        with connection.cursor() as cursor:
            sql = config.get("sql", "sql_movie_search")
            cursor.execute(sql, ('%' + content + '%', '%' + content + '%', '%' + content + '%', (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                v = Movie()
                v.id = result["id"]
                v.type = result["type"]
                v.title = result["title"]
                v.span = result["span"]
                v.update_time = result["update_time"]
                v.play_count = result["play_count"]
                v.play_count *= 31
                v.play_count += 1
                v.horizontal = config.get("server", "img_domain") + result["horizontal"]
                v.vertical = config.get("server", "img_domain") + result["vertical"]
                movie_list.append(json.dumps(v.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return movie_list


def ranking(connection, create_time, movie_type, page, pagesize=20):
    movie_list = []
    try:
        with connection.cursor() as cursor:
            sql = config.get("sql", "sql_movie_ranking")
            cursor.execute(sql, (create_time, movie_type, (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                v = Movie()
                v.id = result["id"]
                v.type = result["type"]
                v.title = result["title"]
                v.span = result["span"]
                v.horizontal = result["horizontal"]
                v.vertical = result["vertical"]
                v.actor = result["actor"]
                v.child_type = result["child_type"]
                v.director = result["director"]
                v.region = result["region"]
                v.year = result["year"]
                v.details = result["details"].decode()
                movie_list.append(json.dumps(v.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return movie_list


def add_count(connection, id):
    try:
        sql = config.get("sql", "sql_movie_add_count")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def info(connection, movie_id):
    movie = None
    try:
        sql = config.get("sql", "sql_query_movie_details")
        with connection.cursor() as cursor:
            cursor.execute(sql, movie_id)
            result = cursor.fetchone()
            if result is not None:
                movie = Movie()
                movie.type = result["type"]
                movie.title = result["title"]
                movie.span = result["span"]
                movie.update_time = result["update_time"]
                movie.horizontal = result["horizontal"]
                movie.vertical = result["vertical"]
                movie.actor = result["actor"]
                movie.child_type = result["child_type"]
                movie.director = result["director"]
                movie.region = result["region"]
                movie.year = result["year"]
                movie.total_part = result["total_part"]
                movie.source = result["source"]
                movie.address = result["address"].decode()
                # movie.details = result["details"].decode()
                movie.play_count = result["play_count"]
                movie.play_count *= 31
                movie.play_count += 1
    except:
        logger.exception(traceback.format_exc())
    return movie


def exist(connection, movie):
    try:
        sql = config.get("sql", "sql_movie_exist")
        with connection.cursor() as cursor:
            cursor.execute(sql, (movie.title, movie.year, movie.type))
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False
