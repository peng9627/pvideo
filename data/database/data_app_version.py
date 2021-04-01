# coding=utf-8
import json
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.app_version import AppVersion

logger = LoggerUtils("data.app_version").logger


def query(connection, type, platform):
    version_result = ''
    try:
        sql = config.get("sql", "sql_query_app_version")
        with connection.cursor() as cursor:
            cursor.execute(sql, (type, platform))
            result = cursor.fetchone()
            if result is not None:
                version = AppVersion()
                version.name = result["name"]
                version.version = result["version"]
                version.details = result["details"]
                version.address = result["address"]
                version.must = result["must"]
                version_result = json.dumps(version.__dict__)

    except:
        logger.exception(traceback.format_exc())
    return version_result
