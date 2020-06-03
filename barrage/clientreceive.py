# coding=utf-8
import Queue
import json
import random
import socket
import struct
import threading
import time
import traceback

import pycore.data.entity.globalvar as gl
from pycore.utils.batch_queue import BatchQueue
from pycore.utils.logger_utils import LoggerUtils

logger = LoggerUtils("barrage_client").logger


class ClientReceive(object):

    def __init__(self):
        self.conns = None
        self.address = None
        self.userId = None
        self.lock = threading.Lock()
        self.sendQueue = BatchQueue()
        self._close = False
        threading.Thread(target=self.relSend, name="clientsend").start()
        self.times = 0
        self.ttime = int(time.time())
        self.redis = gl.get_v("redis")
        self.fire = 0
        self.room = None

    def receive(self, conn, address):
        """
        : 接收
        :param conn:
        :param address:
        :return:
        """
        close = False
        self.conns = conn
        self.address = address

        try:
            while not close:
                length = self.readInt(conn)
                ttime = int(time.time())
                if ttime == self.ttime:
                    self.times += 1
                    if self.times == 10:
                        break
                else:
                    self.times = 0
                    self.ttime = ttime
                if length > 1024:
                    logger.info("packet length more than 1kb")
                    break
                result = self.readBytes(conn, length)
                if length == len(result) and 0 != len(result):
                    base_message = json.loads(result)
                    if 0 == base_message["type"]:
                        self.userId = base_message["uid"]
                        if self.userId in gl.get_v("clients"):
                            gl.get_v("clients")[self.userId].close()
                        gl.get_v("clients")[self.userId] = self
                    elif 1 == base_message["type"]:
                        nick = base_message["nick"]
                        content = base_message["content"]
                        self.sendToAll(json.dumps({"type": 1, "content": nick + " : " + content}))
                    elif 2 == base_message["type"]:
                        nick = base_message["nick"]
                        self.sendToAll(json.dumps({"type": 1, "content": nick + "点赞了主播"}))
                        if self.room is not None:
                            self.fire += random.randint(300, 800)
                            gl.get_v("fire")[self.room] += self.fire
                    elif 3 == base_message["type"]:
                        self.room = base_message["room"]
                        self.fire = random.randint(300, 800)
                        gl.get_v("fire")[self.room] += self.fire
                    else:
                        logger.info("client close")
                else:
                    close = True
                    logger.info("client close")

        except socket.error:
            logger.warning(traceback.format_exc())
        except:
            logger.exception(traceback.format_exc())
        finally:
            self.close()

    def close(self):
        gl.get_v("fire")[self.room] -= self.fire
        self.fire = 0
        if self._close:
            return
        self._close = True
        try:
            if self.conns is not None:
                self.conns.shutdown(socket.SHUT_RDWR)
                self.conns.close()
        except:
            logger.exception(traceback.format_exc())
        if self.userId is not None and self.userId in gl.get_v("clients") and gl.get_v("clients")[self.userId] == self:
            del gl.get_v("clients")[self.userId]
        logger.info("client close")

    def readInt(self, conn):
        msg = self.readBytes(conn, 4)
        data = struct.unpack(">i", msg)
        return data[0]

    def readStringBytes(self, conn):
        length = self.readInt(conn)
        return self.readBytes(conn, length)

    def readBytes(self, conn, length):
        result = bytes()
        while length != 0:
            result1 = conn.recv(length)
            if result1:
                result += result1
                length -= len(result1)
            else:
                logger.info("client close")
                break
        return result

    def write(self, data):
        datalen = struct.pack(">i", len(data))
        self.conns.sendall(datalen)
        self.conns.sendall(data)

    def relSend(self):
        while not self._close:
            try:
                datas = self.sendQueue.getall(20, True, 20)
                for data in datas:
                    datalen = struct.pack(">i", len(data))
                    self.conns.sendall(datalen)
                    self.conns.sendall(data)
            except Queue.Empty:
                logger.info("Received timeout")
            except:
                logger.exception(traceback.format_exc())

    def send(self, data):
        if len(data) > 0:
            self.lock.acquire()
            self.sendQueue.put(data)
            self.lock.release()

    def sendToAll(self, data):
        for (k, v) in gl.get_v("clients").items():
            v.send(data)
