# coding=utf-8
import logging
import re
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, has_request_context, request
from flask_socketio import SocketIO
from pycore.data.entity import config, globalvar as gl
from pycore.utils.redis_utils import RedisUtils

config.init("./conf/pyg.conf")
gl.init()

from api import api, message
from app_thread import reset_count, video_url_ping

app = Flask(__name__)
redis = RedisUtils()
gl.set_v("redis", redis)
gl.set_v("clients", {})
gl.set_v("fire", {})
gl.set_v("onlines", {})
app.secret_key = "l0pgtb2k4lfstpuau672q4f67c7cyrsj"
log_fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(
    filename='./logs/flask.log', when="H", interval=1, backupCount=24)
log_file_handler.suffix = "%Y-%m-%d_%H.log"
log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
log_file_handler.setFormatter(formatter)
log_file_handler.setLevel(logging.INFO)
logger = logging.getLogger('werkzeug')
logger.addHandler(log_file_handler)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
app.register_blueprint(api)

reset_count.reset_count()
# video_url_ping.video_url_ping()
# 弹幕
# threading.Thread(target=server.start, name='barrage_server').start()  # 线程对象.

socketio = SocketIO(app, cors_allowed_origins="*")
socketio.on_event('message', message.on_message)
socketio.on_event('connect', message.on_connect)
socketio.on_event('disconnect', message.on_disconnect)

# socketio.run(app, host="0.0.0.0", port=5000)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super(self).format(record)
