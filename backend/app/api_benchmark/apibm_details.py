#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  apibm_details.py
  * @author:  luozeyu01
  * @date  2023/3/15 6:15 PM
  * @brief 
  *
  **************************************************************************/
"""

import asyncio
import json

from views.base_view import MABaseView
from models.api_benchmark import Job


class ApiBenchmarkDetails(MABaseView):
    """
    执行页面任务执行状况查询
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        id = kwargs.get("id")
        data = await Job.aio_get_object(order_by=None, group_by=None, id=id)
        res_data = {
            "id": data["id"],
            "uid": data["uid"],
            "status": data["status"],
            "description": data["description"],
            "routine": data["routine"],
            "wheel_link": str(data["wheel_link"]),
            "comment": data["comment"],
            "framework": data["framework"],
            "commit": data["commit"],
            "version": data["version"],
            "hostname": data["hostname"],
            "place": data["place"],
            "enable_backward": data["enable_backward"],
            "python": data["python"],
            "yaml_info": data["yaml_info"],
            "system": data["system"],
            "cuda": data["cuda"],
            "cudnn": data["cudnn"],
            "snapshot": data["snapshot"],
            "create_time": str(data["create_time"]),
            "update_time": str(data["update_time"]),
        }

        return 1, res_data

