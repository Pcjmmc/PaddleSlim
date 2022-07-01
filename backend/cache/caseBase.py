# !/usr/bin/env python3
# encoding: utf-8
"""
Cache 的基类定义
"""
from libs.redis.db import redis_pools

class CacheBase(object):
    """
    约定缓存的host、类型、keyname等信息
    """
    host = ""
    data_type = "string"
    key_format = ""

    @classmethod
    def get_pools(cls):
        """
        根据host 获取相应的redis链接
        """
        return redis_pools.get(cls.host)

