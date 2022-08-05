# encoding=utf-8
import asyncio
import copy
import datetime
import json
import time

from models.release_version import CeReleaseVersion
from utils.change_time import stmp_by_date

from views.base_view import MABaseView


class PublishVersionManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        open_cache: 是否从缓存获取，默认False
        根据版本获取汇总信息
        """
        print("requests data", kwargs)
        return 0, []



class PublishTaskManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        # 根据查询需求将版本的相关信息以及steps信息返回到前端
        print("requests data", kwargs)
        version = kwargs.get("version")
        # 如果是dev则返回空即可
        if version == "develop":
            return 0, []
        verison_info = await CeReleaseVersion().aio_get_object(**{"name": version})
        tag = verison_info.tag
        # 根据tag去获取更多的任务详情
        print(kwargs)
        print(tag)
        return 0, []
