from pycore.utils import http_utils


def get_ip(environ):
    ip = None
    if "HTTP_X_FORWARDED_FOR" in environ:
        ip = environ["HTTP_X_FORWARDED_FOR"]
        if len(ip) > 0:
            ip = ip.split(",")[0]
    if ip is None or len(ip) == 0:
        ip = http_utils.getClientIP(environ)
    return ip
