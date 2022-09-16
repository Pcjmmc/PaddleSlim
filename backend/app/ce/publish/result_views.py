# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import copy
import datetime
import json
import time

from libs.mongo.db import Mongo
from models.publish_result import PubishResult

from views.base_view import MABaseView


class PublishResultManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        返回发布结果
        """
        data = {
            'other': [],
            'bos': []
        }
        version = kwargs.get('version')
        appid = kwargs.get('appid', 1)
        print(version)
        # 将bos 以及其他的数据都返回
        table_name_bos = 'publish_bos_{version}_{appid}'.format(
            version=version, appid=appid
        )
        table_name_other = 'publish_other_{version}_{appid}'.format(
            version=version, appid=appid
        )
        table_result = Mongo("paddle_quality", table_name_other)
        result = await table_result.find_all()
        for res in result:
            res.pop('_id')
            for k, v in res.items():
                for k1, v1 in v.items():
                    for k2, v2 in v1.items():
                        tmp = {'source': k, 'system': k1, 'content': {k2: v2}}
                        data['other'].append(tmp)
        return len(data), data
                