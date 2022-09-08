# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import copy
import datetime
import json
import time

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
        返回发布结果 TODO
        """
        defaultData ={
            "Pypi": {"source": 'Pypi', "content": '', "url": ''},
            "Conda": {"source": 'Conda', "content": '', "url": ''},
            "Docker": { "source": 'Docker', "content": '', "url": ''}
        }
        tag = kwargs.get("tag")
        result = await PubishResult.aio_filter_details(**{"tag": tag})
        if result:
            # 将result 和 defaultData合并
            for res in result:
                source = res.get("source")
                defaultData.update({source: res})
        result = [val for key, val in defaultData.items()]
        return len(result), result

    async def post(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        await PubishResult.aio_insert(validated_data=kwargs)

    async def put(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().put(**kwargs)

    async def put_data(self, **kwargs):
        _id = kwargs.get("id")
        kwargs.pop("id")
        await PubishResult.aio_update(
            validated_data=kwargs, params_data={"id": _id}
        )

