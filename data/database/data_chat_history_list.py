# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("data.chat_history_list").logger


def add(connection, user_id, to_id, last_time, content, unread):
    try:
        if not exist(connection, user_id, to_id):
            sql = config.get("sql", "sql_add_chat_history_list")
            with connection.cursor() as cursor:
                cursor.execute(sql, (user_id, to_id, last_time, content))
                connection.commit()
        elif unread:
            sql = config.get("sql", "sql_update_chat_history_list_unread")
            with connection.cursor() as cursor:
                cursor.execute(sql, (last_time, content, user_id, to_id))
                connection.commit()
        else:
            sql = config.get("sql", "sql_update_chat_history_list")
            with connection.cursor() as cursor:
                cursor.execute(sql, (last_time, content, user_id, to_id))
                connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def exist(connection, user_id, to_id):
    try:
        sql = config.get("sql", "sql_chat_history_list_exist")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, to_id))
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False


def receive(connection, user_id, to_id):
    try:
        sql = config.get("sql", "sql_receive_chat_history_list")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, to_id))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def delete(connection, user_id, to_id):
    try:
        sql = config.get("sql", "sql_delete_chat_history_list")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, to_id))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def query(connection, user_id, page, pagesize=12):
    chat_history_list = []
    try:
        with connection.cursor() as cursor:
            sql = config.get("sql", "sql_query_chat_history_list")
            cursor.execute(sql, (user_id, (page - 1) * pagesize, pagesize))
            r = cursor.fetchall()
            for result in r:
                chat_history_list.append(json.dumps(
                    {'to_id': result["to_id"], 'last_time': result["last_time"], 'content': result["content"],
                     'unread': result["unread"]}))
    except:
        logger.exception(traceback.format_exc())
    return chat_history_list
