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
        query = self.get_query(kwargs, self._cookies.get("userid", 0))
        data = await Job.aio_filter_details(**query)
        count = await Job.aio_filter_count(**query)
        for d in data:
            d["create_time"] = str(d.get("create_time"))
            d["update_time"] = str(d.get("update_time"))
        return count, data

    def get_query(self, kwargs, userid=None, level=80):
        """
        构造查询
        """
        query = {key: val for key, val in kwargs.items() if val}
        if "description" in query.keys():
            query["description__contains"] = query["description"]
            del(query["description"])
        if "begin_time" in query.keys():
            query["create_time__gte"] = query["begin_time"]
            del (query["begin_time"])
        if "end_time" in query.keys():
            query["create_time__lte"] = query["end_time"]
            del (query["end_time"])

        if level < 90:
            query = dict({"uid": userid}, **query)
        query = dict({"order_by": "-id"}, **query)
        print(query)
        return query