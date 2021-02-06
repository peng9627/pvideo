import traceback

from flask import request
from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from utils import project_utils
from utils.s3object import S3Object

logger = LoggerUtils('api.file').logger


def upload():
    result = '{"state":-1}'
    code, sessions = project_utils.get_auth(request.headers.environ)
    if 0 == code:
        account_id = sessions["id"]
        data = request.form

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
        result = '{"state":%d}' % code
    return result


def get_address():
    result = '{"state":-1}'
    data = request.form
    try:
        type = data["type"]
        if type == "cover":
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
                account_id = sessions["id"]
                filename = "cover/%s" % (str(account_id) + ".jpg")
                s3client = S3Object()
                if s3client.exist("niunai", filename):
                    result = '{"state":0,"data":"%s/%s"}' % (config.get("server", "live_res_url"), filename)
                else:
                    result = '{"state":3}'
            else:
                result = '{"state":%d}' % code
    except:
        logger.exception(traceback.format_exc())
    return result
