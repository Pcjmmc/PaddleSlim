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

class TaskCacheBase(CacheBase):
    """
    缓存指定版本的所有注册的任务；供首页查询需要
    """
    host = "paddle_quality"
    data_type = "hash"
    key_format = "{version}:{app_id}:all:task"

    @classmethod
    def get_key(cls, version, app_id=1):
        return cls.key_format.format(
            version=version, app_id=app_id
        )

    @classmethod
    async def set_value(cls, key, value, version, app_id=1):
        """
        set data
        """
        key_name = cls.get_key(version, app_id)
        with await cls.get_pools() as redis_conn:
            await redis_conn.hset(key_name, key, value)

    @classmethod
    async def set_multi(cls, version, app_id=1, data=dict()):
        """
        set multi data
        """
        key_name = cls.get_key(version, app_id)
        with await cls.get_pools() as redis_conn:
            await redis_conn.hmset_dict(key_name, data)

    @classmethod
    async def get_value_by_key(cls, key, version, app_id=1):
        """
        get data by key
        """
        res = None
        key_name = cls.get_key(version, app_id)
        with await cls.get_pools() as redis_conn:
            res = await redis_conn.hget(key_name, key)
        
        return res

    @classmethod
    async def get_all_data(cls, version, app_id=1):
        """
        get all data
        """
        res = {}
        key_name = cls.get_key(version, app_id)
        with await cls.get_pools() as redis_conn:
            res = await redis_conn.hgetall(key_name)
        return res

