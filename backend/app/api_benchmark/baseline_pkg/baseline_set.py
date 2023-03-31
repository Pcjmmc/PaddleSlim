#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  baseline_set.py
  * @author:  luozeyu01
  * @date  2023/3/24 1:25 PM
  * @brief 将某一Job的routine设置为0或1
  *
  **************************************************************************/
"""

import asyncio
import json
import datetime

from exception import HTTP400Error
from views.base_view import MABaseView
from models.api_benchmark import Job
from models.user import User
from app.api_benchmark.config.service_url import API_BENCHMARK_SUPERUSER
from utils.change_time import get_begin_and_time


class BaselineSet(MABaseView):
    """
    任务初始化
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        # 获取cookie信息
        uid = self._cookies.get("userid", 0)
        if uid == 0:
            raise HTTP400Error("未登录用户, 没有权限标记基线数据")
        else:
            user = await User.aio_filter_details(id=uid)
            username = user[0]["username"]
            if len(user) == 0:
                raise HTTP400Error("游客用户, 没有权限标记基线数据")
            else:
                if username in API_BENCHMARK_SUPERUSER:
                    id = kwargs.get('id')
                    routine = kwargs.get('routine')
                    if routine == "1":
                        res = await Job.aio_update({"routine": 1}, {"id": id})
                        return res
                    elif routine == "0":
                        res = await Job.aio_update({"routine": 0}, {"id": id})
                        return res
                else:
                    raise HTTP400Error("该用户不是管理员, 没有权限标记基线数据")