#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
  * @file:  apibm_callback.py
  * @author:  luozeyu01
  * @date  2023/2/24 11:17 AM
  * @brief
  *
  **************************************************************************/
"""

from views.base_view import MABaseView
from models.api_benchmark import Job
from exception import HTTP400Error
from datetime import datetime


class ApiBenchmarkCallback(MABaseView):
    """
    mission 回调函数
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        mission 回调函数
        """
        id = kwargs.get("id")
        status = kwargs.get("status")
        result = kwargs.get("result")
        info = kwargs.get("info")
        data = {
            "id": id,
            "status": status,
            "update_time": datetime.now()
        }
        res = await Job.aio_update(data, {"id": id})
        if res == 0:
            raise HTTP400Error("回调数据有问题")
        # apibm_mission = await ApiBenchmarkMission.aio_get_object(id=id)
        return res