# coding=utf-8
import traceback

from pycore.data.entity import config
from pycore.utils.logger_utils import LoggerUtils

from mode.recommend_movie import RecommendMovie

logger = LoggerUtils("data.recommend").logger


def query(connection):
    recommends = []
    try:
        sql = config.get("sql", "sql_recommend_movie")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchall()
            for result in r:
                recommend = RecommendMovie()
                recommend.id = result["id"]
                recommend.ids = result["ids"]
                recommend.desc = result["desc"]
                recommend.index = result["index"]
                recommends.append(recommend)
    except:
        logger.exception(traceback.format_exc())
    return recommends
