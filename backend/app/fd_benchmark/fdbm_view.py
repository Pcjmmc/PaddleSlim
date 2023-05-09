#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  fdbm_view.py
  * @author:  luozeyu01
  * @date  2023/3/30 3:41 PM
  * @brief
  *
  **************************************************************************/
"""

import asyncio
import json

from views.base_view import MABaseView
from models.fd_benchmark import Job

from exception import HTTP400Error
from datetime import datetime
from app.fd_benchmark.dispatcher import Dispatcher
# from app.fd_benchmark.config.service_url import framework_map, enable_backward_map, place_map, cuda_map
# from app.fd_benchmark.config.service_url import python_map, system_map, yaml_type_map, yaml_info_map


class FDBenchmarkInitView(MABaseView):
    """
    任务初始化
    """
    RETRY_TIME = 5

    def mission_analyse(self, data):
        """
        模块解析器
        todo： 解析策略
        """
        if not isinstance(data, list):
            raise HTTP400Error
        mission = dict()
        for i in data:
            mission[i] = None
        return str(json.dumps(mission))

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        初始化ApiBenchmark任务

        1. 任务解析器
        2. 初始化快照信息入库
        """
        # 入库参数
        data = {}
        # 示例：mission: ["op_function","external_api_function"]
        mission = json.loads(kwargs.get("mission", ''))

        # data["uid"] = self._cookies.get("userid", 0)
        # #data["description"] = kwargs.get("name")
        # #data["version"] = kwargs.get("value")
        data["status"] = "running"
        data["fork"] = kwargs.get("fork")
        data["branch"] = kwargs.get("branch")
        data["mission"] = self.mission_analyse(mission)
        data["bos_path"] = kwargs.get("bos_path")
        data["create_time"] = datetime.now()
        data["update_time"] = datetime.now()

        print('data is: ', data)
        res = await Job.aio_insert(data)

        if res[0] == 0:
            raise HTTP400Error
        jid = res[1]
        print('jid is: ', jid)

        # 请求下游服务
        res = await Job.aio_get_object(order_by=None, group_by=None, id=jid)
        await Dispatcher.dispatch_missions(res)

        # retry_time = 5
        # retry = 0
        # while (retry < retry_time):
        #     res = Dispatcher.request_mission("fd_benchmark", id, xly_data)
        #     if isinstance(res, dict):
        #         # 初始化任务
        #         await Job.aio_update({"status": "prepare", "description": str(res)}, {"id": id})
        #         break
        #     else:
        #         await Job.aio_update({"status": "error", "description": res}, {"id": id})
        #         retry += 1

        return {"jid": jid}

    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        id = kwargs.get("id")
        data = await Job.aio_get_object(order_by=None, group_by=None, id=id)
        res_data = {
                "id": data["id"],
                "status": data["status"],
            }
        return 1, res_data
