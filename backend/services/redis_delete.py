# !/usr/bin/env python3
# -*- coding:utf8 -*-
"""
负责打Tag或者删除分支时进行redis key的清理
"""
import asyncio
import os
import sys

import aioredis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from cache.cacheBase import CacheBase


async def clear_redis_keys(prefix="release*"):
    """
    根据prefix清理下缓存数据
    """
    # 只清理release开头的就行；已经发版的不会再变化
    with await CacheBase.get_pools() as redis_conn:
        pipe = redis_conn.pipeline()
        async for key in redis_conn.iscan(match=prefix):
            pipe.delete(key)
        await pipe.execute()



if __name__ == "__main__":
    # 调用示例，初始化menu数据
    loop = asyncio.get_event_loop()
    loop.run_until_complete(clear_redis_keys())

