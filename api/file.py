import traceback

from flask import request
from pycore.data.entity import config, globalvar as gl
from pycore.utils.logger_utils import LoggerUtils

from utils.s3object import S3Object

logger = LoggerUtils('api.file').logger


def upload():
    result = '{"state":-1}'
    data = request.form
    try:
        if "HTTP_AUTH" in request.headers.environ:
            sessionid = request.headers.environ['HTTP_AUTH']
            redis = gl.get_v("redis")
            if not redis.exists(sessionid):
                result = '{"state":2}'
            else:
                sessions = redis.getobj(sessionid)
                account_id = sessions["id"]

                type = data["type"]
                files = request.files
                pic = files["pic"]
                if pic:
                    filename = str(account_id) + ".jpg"
                    pic.save(config.get("server", "img_tmp") + filename)

                    s3client = S3Object()
                    s3client.upload(config.get("server", "img_tmp") + filename, "niunai", type + "/" + filename)
                    result = '{"state":0}'
        else:
            result = '{"state":1}'
    except:
        logger.exception(traceback.format_exc())
    return result


def get_address():
    result = '{"state":-1}'
    data = request.form
    try:
        type = data["type"]
        if type == "cover":
            if "HTTP_AUTH" in request.headers.environ:
                sessionid = request.headers.environ['HTTP_AUTH']
                redis = gl.get_v("redis")
                if not redis.exists(sessionid):
                    result = '{"state":2}'
                else:
                    sessions = redis.getobj(sessionid)
                    account_id = sessions["id"]
                    filename = "cover/%s" % (str(account_id) + ".jpg")
                    s3client = S3Object()
                    if s3client.exist("niunai", filename):
                        result = '{"state":0,"data":"%s/%s"}' % (config.get("server", "live_res_url"), filename)
                    else:
                        result = '{"state":3}'
            else:
                result = '{"state":1}'
    except:
        logger.exception(traceback.format_exc())
    return result
