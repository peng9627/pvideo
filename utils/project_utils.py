from pycore.data.entity import globalvar as gl


def get_auth(environ):
    if "HTTP_AUTH" in environ:
        sessionid = environ['HTTP_AUTH']
        redis = gl.get_v("redis")
        if not redis.exists(sessionid):
            return 2, ''
        else:
            sessions = redis.getobj(sessionid)
            return 0, sessions
    else:
        return 1, ''
