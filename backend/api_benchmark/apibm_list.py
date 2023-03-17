#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
  * @file:  apibm_view.py
  * @author:  luozeyu01
  * @date  2023/2/24 11:17 AM
  * @brief
  *
  **************************************************************************/
"""
import asyncio
import json

from views.base_view import MABaseView
from models.api_benchmark import Job

from views.auth_view import AuthCheck

# DELETE when Release
SuperUser = ["1", "2", "7", "28", "13"]


class ApiBenchmarkList(MABaseView):
    """
    任务初始化
    """

    auth_class = AuthCheck

    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        userid = self._cookies.get("userid", 0)
        # userid = 2333
        query = {"uid": userid}
        query = dict({"order_by": "-id"}, **query)
        data = await Job.aio_filter_details(**query)
        count = await Job.aio_filter_count(**query)
        print(data)
        print(count)
        for d in data:
            d["create_time"] = str(d.get("create_time"))
            d["update_time"] = str(d.get("update_time"))
        return count, data
