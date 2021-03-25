# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.video_history").logger


def add_video_history(connection, video_history):
    try:
        sql = config.get("sql", "sql_exist_video_history")
        with connection.cursor() as cursor:
            cursor.execute(sql, (
                video_history.user_id, video_history.video_id, video_history.video_type))
            result = cursor.fetchone()
            if result["result"] != 0:
                sql = config.get("sql", "sql_update_video_history")
                cursor.execute(sql, (
                    video_history.content, video_history.update_time, video_history.user_id, video_history.video_id,
                    video_history.video_type))
                connection.commit()
            else:
                sql = config.get("sql", "sql_add_video_history")
                cursor.execute(sql, (
                    video_history.user_id, video_history.device, video_history.video_id, video_history.video_type,
                    video_history.update_time, video_history.content))
                connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def query_movie_history(connection, user_id, page, pagesize=12):
    movies = []
    try:
        sql = config.get("sql", "sql_query_movie_history")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, 2, (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                movies.append(json.dumps(
                    {"id": result["id"], "type": result["type"], "title": result["title"], "span": result["span"],
                     "horizontal": result["horizontal"], "vertical": result["vertical"], "content": result["content"],
                     "update_time": result["update_time"]}))
    except:
        logger.exception(traceback.format_exc())
    return movies


def continue_movie_history(connection, user_id, video_id):
    content = ''
    try:
        sql = config.get("sql", "sql_continue_movie_history")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, video_id, 2))
            result = cursor.fetchone()
            if result is not None:
                content = result["content"]
    except:
        logger.exception(traceback.format_exc())
    return content
