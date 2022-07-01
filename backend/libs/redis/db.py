# !/usr/bin/env python3
# -*- coding:utf8 -*-
"""
创建redis连接池
"""
import asyncio
import os
import sys

import aioredis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)

from ce_web.settings.common import STORAGE

redis_cfg = STORAGE["redis"]


class BasePool(object):
    redis_pools = {}
    echo = False

    def __init__(self, env='DEV'):
        # 开发环境
        if env == 'DEV':
            self.echo = True

    async def create_pool(self):
        _redis_pools = {}
        for key, config in redis_cfg.items():
            redis_pool = await aioredis.create_redis_pool(
                (config['host'], config['port']), encoding='utf-8'
            )
            _redis_pools[key] = redis_pool
        self.redis_pools = _redis_pools

    @property
    async def pools(self):
        if not self.redis_pools:
            await self.create_pool()
        return self.redis_pools

loop = asyncio.get_event_loop()
redis_pools = loop.run_until_complete(BasePool().pools)
