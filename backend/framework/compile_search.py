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

class CompileSearch(MABaseView):
    """
    任务初始化
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    # def get_perfect_request_data(self, **kwargs):
    #     return {key: val for key, val in kwargs.items() if val}

    async def get_data(self, **kwargs):
        query = dict({"status": "done"}, **{key: val for key, val in kwargs.items() if val})
        # 只返回查询列表
        data = await Compile.aio_filter_details(need_all=True, **query)
        total = len(data)
        for d in data:
            d["create_time"] = str(d.get("create_time"))
            d["update_time"] = str(d.get("update_time"))
        return total, data