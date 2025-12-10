# coding=utf-8
import traceback

from flask import request
from pycore.data.database import mysql_connection
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_recharge_config
from utils import project_utils

logger = LoggerUtils('api.recharge_config').logger


def list():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        connection = None
        try:
            connection = mysql_connection.get_conn()
            recharge_config = data_recharge_config.list(connection)
            result = '{"state":0, "data":[%s]}' % ",".join(recharge_config)
        except:
            logger.exception(traceback.format_exc())
        finally:
            if connection is not None:
                connection.close()
        return aes_utils.aes_encode(result, key)
    return result
