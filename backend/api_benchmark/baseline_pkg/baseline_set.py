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


from views.base_view import MABaseView
from models.api_benchmark import Job
from utils.change_time import get_begin_and_time


class BaselineSet(MABaseView):
    """
    任务初始化
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        id = kwargs.get('id')
        routine = kwargs.get('routine')
        if routine == "1":
            res = await Job.aio_update({"routine": 1}, {"id": id})
        elif routine == "0":
            res = await Job.aio_update({"routine": 0}, {"id": id})

        return 1, res