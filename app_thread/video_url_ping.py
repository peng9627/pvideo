# coding=utf-8
import threading
import traceback

from pycore.data.database import mysql_connection
from pycore.utils.logger_utils import LoggerUtils

from utils import movie_get_rel_addr

logger = LoggerUtils('app_thread.video_url_ping').logger


def func():
    connection = None
    try:
        connection = mysql_connection.get_conn()
        movie_get_rel_addr.check_adds('http://www.iqiyi.com/v_rzi6cicfvg.html')

    except:
        logger.exception(traceback.format_exc())
    finally:
        if connection is not None:
            connection.close()
    video_url_ping()


def video_url_ping():
    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(1800, func)
    timer.start()
