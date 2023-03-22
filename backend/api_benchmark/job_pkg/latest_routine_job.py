#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  latest_routine_job.py
  * @author:  luozeyu01
  * @date  2023/3/21 2:46 PM
  * @brief 
  *
  **************************************************************************/
"""

import asyncio
import json
import datetime


from views.base_view import MABaseView
from models.api_benchmark import Job
from utils.change_time import get_begin_and_time


class LatestRoutineJob(MABaseView):
    """
    任务初始化
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        query = {
            'routine': 1,
            'status': 'done'
        }
        latest_routine_list = await Job.aio_filter_details(limit=1, order_by='-create_time', **query)
        latest_routine_job = latest_routine_list[0]
        latest_routine_job["create_time"] = str(latest_routine_job.get("create_time"))
        latest_routine_job["update_time"] = str(latest_routine_job.get("update_time"))
        return 1, latest_routine_job