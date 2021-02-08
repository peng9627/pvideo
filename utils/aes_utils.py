# 加密
import base64
import traceback

from Crypto.Cipher import AES
from pycore.utils.stringutils import StringUtils


def new_keys(length):
    return StringUtils.randomStr(length)


# 解密
def aes_decode(data: str, key: str):
    decrypted_text = ''
    try:
        aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)  # 初始化加密器
        decrypted_text = aes.decrypt(base64.b64decode(data.encode('utf-8'))).decode("utf8")  # 解密
        decrypted_text = decrypted_text.rstrip('\0')
    except:
        print(traceback.format_exc())
    return decrypted_text


# 加密
def aes_encode(data: str, key: str):
    count = len(data.encode('utf-8'))
    if (count % 16 != 0):
        add = 16 - (count % 16)
    else:
        add = 0  # 看看你们对接是满16的时候加上16还是0.这里注意
    data = data + ('\0' * add)
    data = data.encode('utf-8')
    aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)  # 初始化加密器
    return base64.b64encode(aes.encrypt(data)).decode('utf-8').replace('\n', '')  # 加密


if __name__ == '__main__':
    msg = '{"type": 2}'
    key = '0s80qxxaxm4o8y4q'
    s = aes_encode(msg, key)
    print(s)
    s = aes_decode(s, key)
    print(s)
