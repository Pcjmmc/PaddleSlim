#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
  * @file:  dispatcher.py
  * @author:  luozeyu01
  * @date  2023/2/24 11:17 AM
  * @brief
  *
  **************************************************************************/
"""

import asyncio
import json

from api_benchmark.apibm_xly.config.service_url import Cloud, CloudMission, DOCKER_IMAGE, CLOUD, PLACE
import api_benchmark.apibm_xly.config.status as STATUS
from api_benchmark.apibm_xly.utils.xly import XlyOpenApiRequest


class Dispatcher(object):
    """
    调度器
    """
    @classmethod
    def cloud_run(cls, module, id, data):
        """
        触发效率云
        """
        xly_agent = XlyOpenApiRequest()
        pipelineid = module
        url_param = "pipelineId={}".format(pipelineid)
        spec_param = {}
        # 构建效率云参数
        params = {
            "id": str(id),
            "comment": data.get('comment'),
            "with_gpu": data.get('with_gpu'),
            "enable_backward": data.get('enable_backward'),
            "framework": data.get('framework'),
            "wheel_link": data.get('wheel_link'),
            "cuda": data.get('cuda'),
            "docker_image": DOCKER_IMAGE.get(data.get('cuda')),
            "python": data.get('python'),
            "yaml_info": data.get('yaml_info'),
        }
        total_param = dict(spec_param, **params)
        data = {
            "branch": "develop",
            "ciType": "MERGE",
            "params": json.dumps(total_param)
        }
        data = json.dumps(data)
        url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipeline-builds?pipelineId={}".format(pipelineid)
        res = xly_agent.post_method(url, data, param=url_param)
        if res.status_code != 200:
            print(res)
            print(res.content.decode('utf-8'))
            return STATUS.ERROR_800 + "错误码：" + str(res.status_code) + res.content.decode('utf-8')
        else:
            print(res.json())
            return res.json()

    @classmethod
    def request_mission(self, module, id, data):
        # todo: 请求任务 任务环境，编译内容，发送请求给效率云
        if PLACE.get(module) is not None:
            if PLACE.get(module) == CLOUD:
                # todo: 效率云的请求发送
                return self.cloud_run(CloudMission.ROUTER.get(module), id, data)
            else:
                return STATUS.ERROR_233
        else:
            # todo: 其他策略
            return STATUS.ERROR_133
