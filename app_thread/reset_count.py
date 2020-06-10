# coding=utf-8
import threading
import time
import traceback

from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl
from pycore.utils import time_utils
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_agent

logger = LoggerUtils('app_thread.reset_count').logger


def func():
    redis = gl.get_v("redis")
    connection = None
    try:
        keys = redis.keys('device_info_*')
        if keys is not None and len(keys) > 0:
            redis.delobj(*keys)
        connection = mysql_connection.get_conn()
        data_agent.reset_min(connection)
    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    reset_count()


def reset_count():
    t = time.time() + 86400
    time_string = time_utils.stamp_to_string(t, '%Y/%m/%d')
    time_stamp = time_utils.string_to_stamp(time_string, '%Y/%m/%d')

    # 获取距离明天0点时间，单位为秒
    timer_start_time = time_stamp - time.time()

    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, func)
    timer.start()
