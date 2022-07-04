# !/usr/bin/env python3
# encoding: utf-8
"""
benchmark的缓存定义
"""
import json

import aioredis

from cache.cacheBase import CacheBase


class BenchmarkCase(CacheBase):
    """
    benchmark的缓存定义
    """
    host = "paddle_quality"
    data_type = "string"
    key_format = 'api:benchmark:config'

    @classmethod
    async def set_value(cls, value):
        """
        set data
        """
        if type(value) != str:
            value = json.dumps(value)
        with await cls.get_pools() as redis_conn:
            await redis_conn.set(cls.key_format, value)

    @classmethod
    async def get_value(cls):
        """
        get data
        """
        result = ""
        with await cls.get_pools() as redis_conn:
            res = await redis_conn.get(cls.key_format)
        try:
            result =json.loads(res)
        except:
            result = res
        return result

    