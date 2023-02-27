# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.agent import Agent

logger = LoggerUtils("data.agent").logger


def by_id(connection, id):
    result = None
    try:
        sql = config.get("sql", "sql_agent_by_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            r = cursor.fetchone()
            if r is not None:
                agent = Agent()
                agent.user_id = id
                if "agent_id" in r and r["agent_id"] is not None:
                    agent.agent_id = r["agent_id"]
                agent.agent_ids = r["agent_ids"]
                agent.top_id = r["top_id"]
                agent.status = r["status"]
                result = agent
    except:
        logger.exception(traceback.format_exc())
    return result


def create(connection, agent):
    result = False
    try:
        sql = config.get("sql", "sql_create_agent")
        with connection.cursor() as cursor:
            cursor.execute(sql, (agent.create_time, agent.user_id, agent.agent_id, agent.agent_ids, agent.top_id))
            connection.commit()
            result = True
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())
    return result


def get_agent_id(connection, id):
    result = None
    try:
        sql = config.get("sql", "sql_agent_get_agent_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            r = cursor.fetchone()
            if r is not None:
                result = r["agent_id"]
    except:
        logger.exception(traceback.format_exc())
    return result


def join(connection, user_id, agent_id):
    try:
        sql = config.get("sql", "sql_agent_join")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, agent_id))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def user_count(connection, id):
    result = 0
    try:
        sql = config.get("sql", "sql_agent_user_count")
        with connection.cursor() as cursor:
            cursor.execute(sql, '%' + str(id) + '%')
            r = cursor.fetchone()
            if r is not None:
                result = r["result"]
    except:
        logger.exception(traceback.format_exc())
    return result


def directly_count(connection, id):
    result = 0
    try:
        sql = config.get("sql", "sql_agent_directly_count")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            r = cursor.fetchone()
            if r is not None:
                result = r["result"]
    except:
        logger.exception(traceback.format_exc())
    return result


def today_new(connection, id, time_stamp):
    result = 0
    try:
        sql = config.get("sql", "sql_agent_today_new")
        with connection.cursor() as cursor:
            cursor.execute(sql, ('%' + str(id) + '%', time_stamp))
            r = cursor.fetchone()
            if r is not None:
                result = r["result"]
    except:
        logger.exception(traceback.format_exc())
    return result


def today_active(connection, id, time_stamp):
    result = 0
    try:
        sql = config.get("sql", "sql_agent_today_active")
        with connection.cursor() as cursor:
            cursor.execute(sql, ('%' + str(id) + '%', time_stamp))
            r = cursor.fetchone()
            if r is not None:
                result = r["result"]
    except:
        logger.exception(traceback.format_exc())
    return result
