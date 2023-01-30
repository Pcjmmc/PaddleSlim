# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from models.project import Project

from views.base_view import MABaseView


class AssociatedManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        根据测试任务ID，获取到icafe的详情，将该任务跟测试任务关联起来
        """
        test_id = kwargs.get("test_id")
        result = await Project.aio_get_object(**{'test_id': test_id})
        res = {"icafe_id": result.get("icafe_id")} if result else {}
        # 将result转换成字典
        return len(res), res

