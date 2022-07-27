# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from models.tasks import CeTasks

from views.base_view import MABaseView


class JobManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        page = kwargs.get("page", 1)
        pagesize = kwargs.get("pagesize", 30)
        appid = kwargs.get("appid", 1)
        query_params = {"appid": appid}
        owner = kwargs.get("owner")
        task_type = kwargs.get("task_type")
        build_type_id = kwargs.get("build_type_id")
        need_all = bool(kwargs.get("need_all", False))
        if owner:
            query_params["owner"] = owner
        if task_type:
            query_params["task_type"] = task_type
        if build_type_id:
            query_params["build_type_id"] = build_type_id
        count, data = await CeTasks().aio_filter_details_with_total_count(
            page_index=page, limit=pagesize, **query_params, need_all=need_all
        )
        for item in data:
            if item['secondary_type']:
                secondarys = item['secondary_type'].split(",")
                # 如果是多选，就返回数组
                if len(secondarys) > 1:
                    item['secondary_type'] = secondarys
        return count, data


    async def post(self, **kwargs):
        """
        调用基类的post方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        await CeTasks().aio_insert(validated_data=kwargs)

    async def put(self, **kwargs):
        """
        调用基类的put方法
        """
        return await super().put(**kwargs)

    async def put_data(self, **kwargs):
        tid = kwargs.get("id")
        kwargs.pop("id")
        await CeTasks().aio_update(
            validated_data=kwargs, params_data={"id": tid}
        )
 

    async def delete(self, **kwargs):
        """
        调用基类的delete方法
        """
        return await super().delete(**kwargs)

    async def delete_data(self, **kwargs):
        tid = kwargs.get("id")
        await CeTasks().aio_delete(params_data={"id": tid})

