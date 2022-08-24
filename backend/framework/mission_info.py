#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile
from exception import HTTP400Error
from datetime import datetime
from framework.dispatcher import Dispatcher
from framework.config.service_url import COMPILE_SERVICE
import requests

class MissionInfo(MABaseView):
    """
    任务初始化
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        mission_id = kwargs.get("id")
        res = await Mission.aio_filter_details(need_all=True, id=mission_id)
        if res is not None:
            data = res[0]
            data["create_time"] = str(data.get("create_time"))
            data["update_time"] = str(data.get("update_time"))
            return 1, data
        else:
            raise HTTP400Error("未查询到数据")
