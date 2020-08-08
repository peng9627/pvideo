# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.feedback").logger


def add_feedback(connection, feedback):
    try:
        sql = config.get("sql", "sql_create_feedback")
        with connection.cursor() as cursor:
            cursor.execute(sql, (feedback.user_id, feedback.title, feedback.content, feedback.create_time))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def query(connection, user_id, page, pagesize=20):
    feedbacks = []
    try:
        sql = config.get("sql", "sql_feedback_list")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                feedbacks.append(json.dumps(
                    {"id": result["id"], "title": result["title"], "create_time": result["create_time"],
                     "status": result["status"]}))
    except:
        logger.exception(traceback.format_exc())
    return feedbacks


def by_id(connection, feedback_id):
    feedback = None
    try:
        sql = config.get("sql", "sql_feedback_by_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, feedback_id)
            result = cursor.fetchone()
            if result is not None:
                feedback = json.dumps(
                    {"title": result["title"], "content": result["content"], "create_time": result["create_time"],
                     "reply_time": result["reply_time"], "reply": result["reply"], "status": result["status"]})
    except:
        logger.exception(traceback.format_exc())
    return feedback
