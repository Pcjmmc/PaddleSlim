import json

import aioredis

from cache.caseBase import CacheBase


class BenchmarkCase(CacheBase):
    host = "paddle_quality"
    data_type = "string"
    key_format = 'api:benchmark:config'

    @classmethod
    async def set_value(cls, value):
        if type(value) != str:
            value = json.dumps(value)
        with await cls.get_pools() as redis_conn:
            await redis_conn.set(cls.key_format, value)

    @classmethod
    async def get_value(cls):
        result = ""
        with await cls.get_pools() as redis_conn:
            res = await redis_conn.get(cls.key_format)
        try:
            result =json.loads(res)
        except:
            result = res
        return result

    