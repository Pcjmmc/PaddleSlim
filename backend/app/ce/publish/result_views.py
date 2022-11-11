# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import copy
import datetime
import json
import time

from libs.mongo.db import Mongo
from models.publish_result import PubishResult
from views.auth_view import AuthCheck
from views.base_view import MABaseView


class PublishResultManage(MABaseView):

    auth_class = AuthCheck
    
    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        返回发布结果
        """
        data = []
        version = kwargs.get('version')
        appid = kwargs.get('appid', 1)
        result = []
        table_name_other = 'publish_other_{version}_{appid}'.format(
            version=version, appid=appid
        )
        table_result = Mongo("paddle_quality", table_name_other)
        other_result = await table_result.find_all()
        result.extend(other_result)
        # 将bos 以及其他的数据都返回
        table_name_bos = 'publish_bos_{version}_{appid}'.format(
            version=version, appid=appid
        )
        table_result_bos = Mongo("paddle_quality", table_name_bos)
        bos_result = await table_result_bos.find_all()
        result.extend(bos_result)
        for res in result:
            res.pop('_id')
            for k, v in res.items():
                for k1, v1 in v.items():
                    for k2, v2 in v1.items():
                        tmp = {'source': k, 'system': k1, 'content': {k2: v2}}
                        data.append(tmp)
        return len(data), data
                