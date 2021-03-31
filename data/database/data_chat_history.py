# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.chat_history").logger


def create_chat_history(connection, chat_history):
    try:
        sql = config.get("sql", "sql_create_chat_history")
        with connection.cursor() as cursor:
            cursor.execute(sql,
                           (chat_history.user_id, chat_history.to_id, chat_history.create_time, chat_history.content))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def receive_chat_history(connection, receive_time, create_time, user_id, to_id):
    try:
        sql = config.get("sql", "sql_receive_chat_history")
        with connection.cursor() as cursor:
            cursor.execute(sql, (receive_time, create_time, user_id, to_id))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def clean_chat_history(connection, user_id, to_id):
    try:
        sql = config.get("sql", "sql_clean_chat_history")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, to_id))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def query_chat_history(connection, user_id, to_id, create_time, page=1, pagesize=12):
    chat_history_list = []
    try:
        with connection.cursor() as cursor:
            sql = config.get("sql", "sql_query_chat_history")
            cursor.execute(sql, (user_id, to_id, user_id, to_id, create_time, (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                chat_history_list.append(
                    json.dumps({'user_id': result["user_id"], 'create_time': result["create_time"],
                                'content': result["content"]}))
    except:
        logger.exception(traceback.format_exc())
    return chat_history_list


def unread_count(connection, user_id):
    count = 0
    try:
        sql = config.get("sql", "sql_chat_history_unread_count")
        with connection.cursor() as cursor:
            cursor.execute(sql, user_id)
            result = cursor.fetchone()
            count = result["result"]
    except:
        logger.exception(traceback.format_exc())
    return count
