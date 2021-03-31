from flask import request
from pycore.data.entity import config
from pycore.utils import aes_utils
from pycore.utils.logger_utils import LoggerUtils

from utils import project_utils
from utils.s3object import S3Object

logger = LoggerUtils('api.file').logger


def upload():
    result = '{"state":-1}'
    key = project_utils.get_key(request.headers.environ)
    if key is not None:
        data = request.form["data"]
        data = project_utils.get_data(key, data)
        if data is not None:
            code, sessions = project_utils.get_auth(request.headers.environ)
            if 0 == code:
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
                result = '{"state":%d}' % code
        return aes_utils.aes_encode(result, key)
    return result
