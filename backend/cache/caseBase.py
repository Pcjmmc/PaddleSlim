# encoding: utf-8
from libs.redis.db import redis_pools

class CacheBase(object):
    host = ""
    data_type = "string"
    key_format = ""

    @classmethod
    def get_pools(cls):
        return redis_pools.get(cls.host)

