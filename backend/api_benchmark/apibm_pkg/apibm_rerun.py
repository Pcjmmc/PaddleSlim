#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
  * @file:  apibm_rerun.py
  * @author:  luozeyu01
  * @date  2023/2/24 11:17 AM
  * @brief
  *
  **************************************************************************/
"""

from views.base_view import MABaseView
from models.api_benchmark import ApiBenchmarkMission
from api_benchmark.dispatcher import Dispatcher


class ApiBenchmarkRerun(MABaseView):
    """
    手动标记任务失败
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        重新触发效率云任务
        """
        # 获取apibm数据
        apibm_id = kwargs.get("id")
        apibm_info = await ApiBenchmarkMission.aio_get_object(id=apibm_id)

        # 获取任务信息
        data = {
            "status": apibm_info["status"],
            "comment": apibm_info["comment"],
            "with_gpu": apibm_info["with_gpu"],
            "enable_backward": apibm_info["enable_backward"],
            "framework": apibm_info["framework"],
            "wheel_link": apibm_info["wheel_link"],
            "cuda": apibm_info["cuda"],
            "python": apibm_info["python"],
            "yaml_type": apibm_info["yaml_type"],
            "yaml_info": apibm_info["status"],
            "create_time": apibm_info["create_time"],
            "update_time": apibm_info["update_time"],
        }

        # 触发任务
        retry = 0
        retry_time = 5
        while (retry < retry_time):
            res = Dispatcher.request_mission("api_benchmark", apibm_id, data)
            if isinstance(res, dict):
                #初始化任务
                await ApiBenchmarkMission.aio_update({"status": "running", "description": ""}, {"id": apibm_id})
                return "重新执行成功"
            else:
                await ApiBenchmarkMission.aio_update({"status": "error", "description": res}, {"id": apibm_id})
                retry += 1
        return "重新执行失败"
