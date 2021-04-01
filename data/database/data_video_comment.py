# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.video_comment").logger


def create(connection, comment):
    try:
        sql = config.get("sql", "sql_add_video_comment")
        with connection.cursor() as cursor:
            cursor.execute(sql, (comment.user_id, comment.video_id, comment.create_time, comment.content))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def query(connection, video_id, page, pagesize=20):
    video_comments = []
    try:
        sql = config.get("sql", "sql_query_comment")
        with connection.cursor() as cursor:
            cursor.execute(sql, (video_id, (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                video_comments.append(json.dumps(
                    {"nickname": result["nickname"], "head": '' if result["head"] is None else result["head"],
                     "create_time": result["create_time"], "content": result["content"], }))
    except:
        logger.exception(traceback.format_exc())
    return video_comments


def count(connection, video_id):
    result = 0
    try:
        sql = config.get("sql", "sql_video_comment_count")
        with connection.cursor() as cursor:
            cursor.execute(sql, video_id)
            result = cursor.fetchone()
            result = result["result"]
    except:
        logger.exception(traceback.format_exc())
    return result
