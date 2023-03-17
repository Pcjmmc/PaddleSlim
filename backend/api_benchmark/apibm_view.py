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
from exception import HTTP400Error
from datetime import datetime
from api_benchmark.dispatcher import Dispatcher
from api_benchmark.config.service_url import framework_map, enable_backward_map, place_map, cuda_map
from api_benchmark.config.service_url import python_map, system_map, yaml_type_map, yaml_info_map

class ApiBenchmarkInitView(MABaseView):
    """
    任务初始化
    """
    RETRY_TIME = 5

    def input_build(self, **kwargs):
        """
        构建输入
        """
        input_dict = {}
        input_dict['comment'] = kwargs.get('comment')
        input_dict['place'] = place_map.get(kwargs.get('place'))
        input_dict['routine'] = 0
        input_dict['enable_backward'] = enable_backward_map.get(kwargs.get('enable_backward'))
        input_dict['framework'] = framework_map.get(kwargs.get('framework'))
        input_dict['cuda'] = cuda_map.get(kwargs.get('cuda'))
        input_dict['cudnn'] = 'not_yet'
        input_dict['python'] = python_map.get(kwargs.get('python'))
        input_dict['wheel_link'] = kwargs.get('wheel_link')
        if input_dict['wheel_link'].startswith('https://'):
            if input_dict['cuda'] in input_dict['wheel_link']:
                pass
            elif input_dict['cuda'].replace('v', 'Cuda').replace('.', '') in input_dict['wheel_link']:
                pass
            elif input_dict['cuda'].replace('v', 'post').replace('.', '') in input_dict['wheel_link']:
                pass
            elif input_dict['cuda'].replace('v', 'post') in input_dict['wheel_link']:
                pass
            else:
                raise HTTP400Error("whl包cuda版本和已选择的cuda版本不匹配")

            if input_dict['python'].replace('python', 'cp').replace('.', '') in input_dict['wheel_link']:
                pass
            else:
                raise HTTP400Error("whl包python版本和已选择的python版本不匹配")
        else:
            raise HTTP400Error("请通过QA的编包服务获取正确的wheel包 https:// 链接")

        input_dict['yaml_type'] = yaml_type_map.get(kwargs.get('yaml_type'))
        if yaml_type_map.get(kwargs.get('yaml_type')) == 'default':
            input_dict['yaml_info'] = yaml_info_map.get(kwargs.get('yaml_info'))
        elif yaml_type_map.get(kwargs.get('yaml_type')) == 'diy':
            raise HTTP400Error("暂不支持diy模式配置yaml")  # 占位
        else:
            raise HTTP400Error("未知yaml配置模式")  # 占位

        return input_dict

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        初始化ApiBenchmark任务

        1. 任务解析器
        2. 初始化快照信息入库
        """
        # 入库参数
        params = dict()
        params["uid"] = self._cookies.get("userid", 0)
        # params["uid"] = 2333
        params['system'] = system_map.get(kwargs.get('system'))
        params['commit'] = 'not_yet'
        params["status"] = "prepare"
        params["create_time"] = datetime.now()
        params["update_time"] = datetime.now()

        data = dict(params, **self.input_build(**kwargs))
        # print('data is: ', data)
        res = await Job.aio_insert(data)

        if res[0] == 0:
            raise HTTP400Error
        id = res[1]

        # 效率云参数
        xly_params = dict()
        xly_params["id"] = id
        xly_data = dict(xly_params, **self.input_build(**kwargs))

        retry_time = 5
        retry = 0
        while (retry < retry_time):
            res = Dispatcher.request_mission("api_benchmark", id, xly_data)
            if isinstance(res, dict):
                # 初始化任务
                await Job.aio_update({"status": "prepare", "description": str(res)}, {"id": id})
                break
            else:
                await Job.aio_update({"status": "error", "description": res}, {"id": id})
                retry += 1

        return {"id": id}

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
