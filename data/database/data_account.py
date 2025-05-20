# coding=utf-8
import random
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.account import Account

logger = LoggerUtils("data.account").logger


def create(connection, account, last_address):
    try:
        sql = config.get("sql", "sql_create_account")
        with connection.cursor() as cursor:
            userid = 0
            while userid == 0:
                uid = random.randint(200000, 999999)
                if query_by_id(connection, uid) is None:
                    userid = uid
            cursor.execute(sql, (userid, account.account_name, account.pwd, account.salt, account.nickname,
                                 account.create_time, account.code, account.create_time, last_address, account.device,
                                 account.platform))
            connection.commit()
    except:
        connection.rollback()
        logger.exception(traceback.format_exc())


def device_count(connection, device):
    try:
        sql = config.get("sql", "sql_device_account_count")
        with connection.cursor() as cursor:
            cursor.execute(sql, device)
            result = cursor.fetchone()
            return int(result["result"])
    except:
        logger.exception(traceback.format_exc())
    return False


def query_by_account_name(connection, account_name):
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


def query_id_by_code(connection, code):
    account_id = None
    try:
        sql = config.get("sql", "sql_query_account_id_by_code")
        with connection.cursor() as cursor:
            cursor.execute(sql, code)
            result = cursor.fetchone()
            if result is not None:
                account_id = result["result"]
    except:
        logger.exception(traceback.format_exc())
    return account_id


def query_by_id(connection, id):
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
