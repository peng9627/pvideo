import time
import traceback

from flask import request, session
from flask_socketio import send
from pycore.data.database import mysql_connection
from pycore.data.entity import globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

from data.database import data_chat_history, data_chat_history_list
from mode.chat_history import ChatHistory

logger = LoggerUtils('api.message').logger


def on_message(data):
    # type  0.登录-未读消息条数 1.发送消息-收到消息
    if data['type'] == 0:
        uid = data['data']
        gl.get_v("onlines")[uid] = request.sid
        session['uid'] = uid
        connection = None
        try:
            connection = mysql_connection.get_conn()
            message_count = data_chat_history.unread_count(connection, uid)
            send({'type': 0, 'data': message_count})
        except:
            logger.exception(traceback.format_exc())
        finally:
            if connection is not None:
                connection.close()
    elif data['type'] == 1:
        if 'uid' in session:
            uid = session['uid']
            to_id = data['to']
            content = data['data']
            chat_history = ChatHistory()
            chat_history.user_id = session['uid'] = uid
            chat_history.to_id = to_id
            chat_history.create_time = int(time.time())
            chat_history.content = content
            connection = None
            try:
                connection = mysql_connection.get_conn()
                data_chat_history.create_chat_history(connection, chat_history)
                data_chat_history_list.add_chat_history_list(connection, uid, to_id, chat_history.create_time, content)
                data_chat_history_list.add_chat_history_list(connection, to_id, uid, chat_history.create_time, content)
                send({'type': 1, 'data': content, 'from': uid}, room=gl.get_v("onlines")[to_id])
            except:
                logger.exception(traceback.format_exc())
            finally:
                if connection is not None:
                    connection.close()


def on_connect():
    print('Client connected')


def on_disconnect():
    if 'uid' in session:
        gl.get_v("onlines").pop(session['uid'])
        session.pop('uid')
    print('Client disconnected')
