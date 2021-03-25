# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.http_utils import HttpUtils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_gold
from mode.account import Account

logger = LoggerUtils("data.account").logger


def create_account(connection, account, last_address, share_code, share_ip):
    try:
        sql = config.get("sql", "sql_create_account")
        with connection.cursor() as cursor:
            cursor.execute(sql,
                           (account.account_name, account.pwd, account.salt, account.nickname, account.create_time,
                            account.code, account.create_time, last_address))
            connection.commit()
            account = query_account_by_account_name(connection, account.account_name)
            if account is not None:
                update_gold(connection, int(config.get("server", "register_gold")), account.id)
                data_gold.create_gold(connection, 1, 0, account.id, int(config.get("server", "register_gold")))
                try:
                    s = HttpUtils(config.get("api", "api_host")).post(config.get("api", "bind"),
                                                                      json.loads(config.get("api", "bind_param") % (
                                                                          account.id, share_code, share_ip)))
                    res = s
                except:
                    logger.exception(traceback.format_exc())
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def query_account_by_account_name(connection, account_name):
    account = None
    try:
        sql = config.get("sql", "sql_query_account_by_account_name")
        with connection.cursor() as cursor:
            cursor.execute(sql, account_name)
            result = cursor.fetchone()
            if result is not None:
                account = Account()
                account.id = int(result["id"])
                account.account_name = result["account_name"]
                account.pwd = result["pwd"]
                account.salt = result["salt"]
                if result["head"] is not None:
                    account.head = result["head"]
                account.nickname = result["nickname"]
                account.sex = result["sex"]
                account.create_time = result["create_time"]
                account.last_time = result["last_time"]
                account.last_address = result["last_address"]
                account.account_status = result["account_status"]
                account.device = result["device"]
                account.code = result["code"]
                account.gold = result["gold"]
    except:
        logger.exception(traceback.format_exc())
    return account


def query_account_by_code(connection, code):
    account = None
    try:
        sql = config.get("sql", "sql_query_account_by_code")
        with connection.cursor() as cursor:
            cursor.execute(sql, code)
            result = cursor.fetchone()
            if result is not None:
                account = Account()
                account.id = int(result["id"])
                account.account_name = result["account_name"]
                account.pwd = result["pwd"]
                account.salt = result["salt"]
                if result["head"] is not None:
                    account.head = result["head"]
                account.nickname = result["nickname"]
                account.sex = result["sex"]
                account.create_time = result["create_time"]
                account.last_time = result["last_time"]
                account.last_address = result["last_address"]
                account.account_status = result["account_status"]
                account.device = result["device"]
                account.code = result["code"]
                account.gold = result["gold"]
    except:
        logger.exception(traceback.format_exc())
    return account


def query_account_by_id(connection, id):
    account = None
    try:
        sql = config.get("sql", "sql_query_account_by_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            result = cursor.fetchone()
            if result is not None:
                account = Account()
                account.id = int(result["id"])
                account.account_name = result["account_name"]
                account.pwd = result["pwd"]
                account.salt = result["salt"]
                if result["head"] is not None:
                    account.head = result["head"]
                account.nickname = result["nickname"]
                account.sex = result["sex"]
                account.create_time = result["create_time"]
                account.last_time = result["last_time"]
                account.last_address = result["last_address"]
                account.account_status = result["account_status"]
                account.device = result["device"]
                account.code = result["code"]
                account.gold = result["gold"]
    except:
        logger.exception(traceback.format_exc())
    return account


def update_login(t, connection, address, account):
    try:
        sql = config.get("sql", "sql_update_login")
        with connection.cursor() as cursor:
            cursor.execute(sql, (int(t), address, account))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def update_pwd(connection, pwd, account_id):
    try:
        sql = config.get("sql", "sql_update_pwd")
        with connection.cursor() as cursor:
            cursor.execute(sql, (pwd, account_id))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def exist(connection, account):
    try:
        sql = config.get("sql", "sql_exist")
        with connection.cursor() as cursor:
            cursor.execute(sql, account)
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False


def exist_code(connection, code):
    try:
        sql = config.get("sql", "sql_exist_code")
        with connection.cursor() as cursor:
            cursor.execute(sql, code)
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        logger.exception(traceback.format_exc())
    return False


def update_gold(connection, gold, id):
    try:
        sql = config.get("sql", "sql_update_gold") % (gold, id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def by_parent(connection, parent_id, page, page_size=20):
    users = []
    try:
        sql = config.get("sql", "sql_query_account_by_parent_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, (parent_id, (page - 1) * page_size, page_size))
            r = cursor.fetchall()
            for result in r:
                users.append(
                    '{"id": %d, "nickname": "%s", "create_time": %d, "gold": %d, "status": %d}' % (
                        result["id"], result["nickname"], result["create_time"], result["gold"], result["status"]))
    except:
        logger.exception(traceback.format_exc())
    return users
