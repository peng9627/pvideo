# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.agent.agent import Agent

logger = LoggerUtils("data_agent").logger


def agent_by_id(connection, id):
    result = None
    try:
        sql = config.get("sql", "sql_agent_by_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            r = cursor.fetchone()
            if r is not None:
                agent = Agent()
                agent.user_id = id
                if "parent_id" in r and r["parent_id"] is not None:
                    agent.parent_id = r["parent_id"]
                agent.parent_ids = r["parent_ids"]
                agent.top_id = r["top_id"]
                agent.min = r["min"]
                agent.total_min = r["total_min"]
                agent.status = r["status"]
                agent.contact = r["contact"]
                result = agent
    except:
        logger.exception(traceback.format_exc())
    return result


def add_agent(connection, agent):
    result = False
    try:
        sql = config.get("sql", "sql_add_agent")
        with connection.cursor() as cursor:
            cursor.execute(sql, (
                agent.create_date, agent.user_id, agent.parent_id, agent.parent_ids, agent.top_id, agent.commission,
                agent.total_commission, agent.contact))
            connection.commit()
            result = True
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())
    return result


def add_min(connection, pid):
    try:
        add_min = int(config.get("server", "share_add_min"))
        sql = config.get("sql", "sql_add_min") % (add_min, add_min, pid)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def agent_contact(connection, id):
    result = None
    try:
        sql = config.get("sql", "sql_agent_contact")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            r = cursor.fetchone()
            if r is not None:
                result = r["contact"]
    except:
        logger.exception(traceback.format_exc())
    return result


def agent_get_parent_id(connection, id):
    result = None
    try:
        sql = config.get("sql", "sql_agent_get_parent_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            r = cursor.fetchone()
            if r is not None:
                result = r["parent_id"]
    except:
        logger.exception(traceback.format_exc())
    return result


def join(connection, user_id, parent_id):
    try:
        sql = config.get("sql", "sql_agent_join")
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id, parent_id))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def agent_set(connection, user_id, contact, old_contact):
    try:
        sql = config.get("sql", "sql_agent_set")
        with connection.cursor() as cursor:
            cursor.execute(sql, (contact, user_id, '%' + str(user_id) + '%', old_contact))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def agent_user_count(connection, id):
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


def agent_directly_count(connection, id):
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


def agent_today_new(connection, id, time_stamp):
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


def agent_today_active(connection, id, time_stamp):
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
