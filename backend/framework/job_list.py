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

class JobList(MABaseView):
    """
    任务初始化
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        id = kwargs.get("id")
        description = kwargs.get("name")
        if id is not None:
            data = await Job.aio_filter_details(id=id)
            for d in data:
                d["create_time"] = str(d.get("create_time"))
                d["update_time"] = str(d.get("update_time"))
            return 1, data
        elif description is not None:
            data = await Job.aio_filter_details(description__contains=description)
            for d in data:
                d["create_time"] = str(d.get("create_time"))
                d["update_time"] = str(d.get("update_time"))
            return len(data), data
        else:
            # 只返回查询列表
            page_index = kwargs.get("page_index")
            limit = kwargs.get("limit")
            data = await Job.aio_filter_details(page_index=page_index, limit=limit, order_by="-id")
            total = await Job.aio_filter_count()
            for d in data:
                d["create_time"] = str(d.get("create_time"))
                d["update_time"] = str(d.get("update_time"))
            return total, data
