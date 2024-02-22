# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.recharge_config import RechargeConfig

logger = LoggerUtils('data.recharge_config').logger


def by_id(connection, id):
    recharge_config = None
    try:
        sql = config.get("sql", "sql_recharge_config_by_id")
        with connection.cursor() as cursor:
            cursor.execute(sql, id)
            result = cursor.fetchone()
            if result is not None:
                recharge_config = RechargeConfig()
                recharge_config.id = result["id"]
                recharge_config.name = result["name"]
                recharge_config.create_time = result["create_time"]
                recharge_config.amount = int(result["amount"])
                recharge_config.vip_days = result["vip_days"]
                recharge_config.status = result["status"]
    except:
        logger.exception(traceback.format_exc())
    return recharge_config


def list(connection):
    recharge_config_list = []
    try:
        sql = config.get("sql", "sql_recharge_config_list")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                recharge_config = RechargeConfig()
                recharge_config.id = result["id"]
                recharge_config.name = result["name"]
                recharge_config.create_time = result["create_time"]
                recharge_config.amount = float(result["amount"])
                recharge_config.vip_days = result["vip_days"]
                recharge_config.status = result["status"]
                recharge_config_list.append(json.dumps(recharge_config.__dict__))
    except:
        logger.exception(traceback.format_exc())
    return recharge_config_list
