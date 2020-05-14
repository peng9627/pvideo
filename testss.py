from pycore.utils.stringutils import StringUtils

if __name__ == '__main__':
    salt = StringUtils.randomStr(32)
    password = StringUtils.md5('123456' + salt)
    print salt
    print password
