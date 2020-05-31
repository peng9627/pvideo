import os
import socket
import threading
import traceback

from pycore.data.entity import config, globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

from barrage.clientreceive import ClientReceive

logger = LoggerUtils("barrage_server").logger


def start():
    try:
        ip_port = ('', int(config.get("server", "barrage_port")))
        sk = socket.socket()
        sk.bind(ip_port)
        sk.listen(5)
        logger.info("server started")
        while True:
            conn, address = sk.accept()
            threading.Thread(target=ClientReceive.receive,
                             args=(ClientReceive(), conn, '''%s:%d''' % (address[0], address[1]),),
                             name='clientreceive').start()  # 线程对象.
    except:
        logger.exception(traceback.format_exc())
        for (c, v) in gl.get_v("clients").items():
            v.close()
