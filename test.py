# coding=utf-8

from pycore.data.entity import config, globalvar as gl


config.init("./conf/pyg.conf")
gl.init()

from utils import movie_get_rel_addr
if __name__ == '__main__':
    movie_get_rel_addr.check_adds('http://www.iqiyi.com/v_rzi6cicfvg.html')
