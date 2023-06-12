#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
性能对比工具
"""
import asyncio
import json
from datetime import datetime
import requests
from exception import HTTP400Error

from views.base_view import MABaseView
from models.fd_benchmark import Job, Mission, Case


class JobGetMission(MABaseView):
    """
    输入job id，查询对应的多硬件mission
    """

    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        job_id = kwargs.get('id')
        data = await Mission.aio_filter_details(jid=job_id)
        count = await Mission.aio_filter_count(jid=job_id)
        for d in data:
            d["create_time"] = str(d.get("create_time"))
            d["update_time"] = str(d.get("update_time"))
        print('data', data)
        return count, data
