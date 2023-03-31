# !/usr/bin/env python3
# encoding: utf-8
"""
benchmark的缓存定义
"""
import json

import aioredis

from cache.cacheBase import CacheBase


class ReleaseSummaryCase(CacheBase):
    """
    ReleaseSummary计算结果的缓存
    """
    host = "paddle_quality"
    data_type = "string"
    key_format = '{version}:summary'

    @classmethod
    async def set_value(cls, version, value, expired=0):
        """
        set data
        """
        key_format = cls.key_format.format(version=version)
        if type(value) != str:
            value = json.dumps(value)
        with await cls.get_pools() as redis_conn:
            await redis_conn.set(key_format, value, expire=expired)

    @classmethod
    async def get_value(cls, version):
        """
        get data
        """
        result = ""
        key_format = cls.key_format.format(version=version)
        with await cls.get_pools() as redis_conn:
            res = await redis_conn.get(key_format)
        try:
            result = json.loads(res)
        except:
            result = res
        return result

    