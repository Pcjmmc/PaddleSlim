"""
实现豁免相关的逻辑
"""
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo
from models.exempt import CeExempt

from views.base_view import MABaseView


class ExemptManege(MABaseView):


    async def post(self, **kwargs):
        """
        调用基类的post方法，负责豁免的创建
        """
        return await super().post(**kwargs)


    async def post_data(self, **kwargs):
        """
        新增一条豁免数据, 存在则修改，不存在则更新 TDDO
        """
        query_data = {
            "version_id": kwargs.get("version_id"),
            "tid": kwargs.get("tid")
        }
        res = await CeExempt().aio_get_object(**query_data)
        if res:
            # 存在则修改
            status = kwargs.get("status") or res.status
            update_data = {
                "status": int(status)
            }
            await CeExempt().aio_update(
                validated_data=update_data,
                params_data=query_data
            )
        else:
            status = kwargs.get("status")
            status = int(status) if status else 1
            kwargs['status'] = status
            await CeExempt().aio_insert(validated_data=kwargs)

    async def put(self, **kwargs):
        """
        调用基类的put方法,负责豁免相关操作的修改
        """
        return await super().put(**kwargs)


    async def put_data(self, **kwargs):
        """
        修改一条豁免数据
        """
        query_data = {
            "version_id": kwargs.get("version_id"),
            "tid": kwargs.get("tid")
        }
        status = kwargs.get("status", None)

        if status is not None:
            status = int(status)
            await CeExempt().aio_update(
                validated_data={"status": status},
                params_data=query_data
            )


    
