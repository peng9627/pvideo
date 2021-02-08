# 加密
import base64

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def new_keys(length):
    private = RSA.generate(length)
    public = private.publickey()
    private_key = private.exportKey()
    public_key = public.exportKey()
    return public_key.decode('utf-8'), private_key.decode('utf-8')


def msg_encrypt(msg: str, pub_key):
    public_key = RSA.importKey(pub_key)
    cipher = PKCS1_v1_5.new(public_key)
    max_msg_length = public_key.size_in_bytes() - 11
    msg_bytes = msg.encode('utf-8')
    secret_bytes = bytes()
    for i in range(0, len(msg_bytes), max_msg_length):
        secret_bytes += base64.b64encode(cipher.encrypt(msg_bytes[i:i + max_msg_length]))
    secret_msg = secret_bytes
    return secret_msg.decode('utf-8')


# 解密
def msg_dencrypt(secret_msg: str, priv_key):
    private_key = RSA.importKey(priv_key)
    cipher = PKCS1_v1_5.new(private_key)
    secret_bytes = base64.b64decode(secret_msg)
    res_msg = bytes()
    max_msg_length = private_key.size_in_bytes()
    for i in range(0, len(secret_bytes), max_msg_length):
        res_msg += cipher.decrypt(secret_bytes[i:i + max_msg_length], b'')
    return res_msg.decode('utf-8')


if __name__ == '__main__':
    mess = 'hello'
    secret_msg = msg_encrypt(mess, open('../conf/public.pem').read())
    print(secret_msg)
    mess = msg_dencrypt(secret_msg, open('../conf/private.pem').read())
    print(mess)
