# !/usr/bin/env python3
# encoding: utf-8
"""
benchmark的缓存定义
"""
import json

import aioredis

from cache.cacheBase import CacheBase


class BuildCacheBase(CacheBase):
    """
    缓存每个任务最新的一次，key是任务的唯一id
    # 这里的build_type_id 与数据库的tid是一一对映的，故直接用tid
    """
    host = "paddle_quality"
    data_type = "hash"
    # 只保留dev以及最新的release分支，注意release不必精确到版本
    # task:tid:latest:build:release
    key_format = "task:{tid}:latest:build:{branch}"

    @classmethod
    async def delete_keys(cls, tid, branch):
        """
        如果已经存在则删除，不存在追究的情况，因为任务的最新一次信息都是一次性存入的
        """
        key = cls.key_format.format(tid=tid, branch=branch)
        with await cls.get_pools() as redis_conn:
            if await redis_conn.exists(key):
                await redis_conn.delete(key)

    @classmethod
    async def set_multi(cls, tid, branch, data=dict()):
        """
        set multi data
        """
        key = cls.key_format.format(tid=tid, branch=branch)
        with await cls.get_pools() as redis_conn:
            await redis_conn.hmset_dict(key, data)

    @classmethod
    async def get_all_data(cls, tid, branch):
        """
        get all data
        """
        res = {}
        key = cls.key_format.format(tid=tid, branch=branch)
        with await cls.get_pools() as redis_conn:
            res = await redis_conn.hgetall(key)
        return res
