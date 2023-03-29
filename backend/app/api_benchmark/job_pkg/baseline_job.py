#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  baseline_job.py
  * @author:  luozeyu01
  * @date  2023/3/24 2:09 PM
  * @brief 通过传入的id返回对应的baseline id
  *
  **************************************************************************/
"""

import asyncio
import json

from views.base_view import MABaseView
from models.api_benchmark import Job, Case
from app.api_benchmark.config.service_url import paddle_develop_version, paddle_release_version, torch_release_version
from exception import HTTP400Error
from datetime import datetime
import requests


class BaselineJob(MABaseView):
    """
    查看version
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        id = kwargs.get('id')
        baseline_type = kwargs.get('baseline_type')
        origin_data = await Job.aio_get_object(id=id)

        query = {
            'routine': 1,
            'status': 'done',
            'cuda': origin_data['cuda'],
            'python': origin_data['python'],
            'system': origin_data['system'],
            # 'enable_backward': origin_data['enable_backward'],
        }
        if baseline_type == 'paddle_develop':
            version_query = {
                'framework': 'paddle',
                'place': origin_data['place'],  # cpu和gpu性能差异较大,所以将place查询优先级提升
                'version': paddle_develop_version,
            }
            paddle_develop_query = dict(query, **version_query)
            data_list = await Job.aio_filter_details(limit=1, order_by='-create_time', **paddle_develop_query)
            if bool(data_list) is False:  # 如果查不到符合所有条件的数据，就使用符合version_query条件的数据
                data_tmp = await Job.aio_filter_details(limit=1, order_by='-create_time', **version_query)
                if bool(data_tmp) is False:
                    raise HTTP400Error("数据库中，相关基线数据缺失")
                else:
                    data = data_tmp[0]
            else:
                data = data_list[0]
                
        elif baseline_type == 'paddle_release':
            version_query = {
                'framework': 'paddle',
                'place': origin_data['place'],  # cpu和gpu性能差异较大,所以将place查询优先级提升
                'version': paddle_release_version,
            }
            paddle_release_query = dict(query, **version_query)
            data_list = await Job.aio_filter_details(limit=1, order_by='-create_time', **paddle_release_query)
            print(data_list)
            if bool(data_list) is False:  # 如果查不到符合所有条件的数据，就使用符合version_query条件的数据
                data_tmp = await Job.aio_filter_details(limit=1, order_by='-create_time', **version_query)
                if bool(data_tmp) is False:
                    raise HTTP400Error("数据库中，相关基线数据缺失")
                else:
                    data = data_tmp[0]
            else:
                data = data_list[0]

        # elif baseline_type == 'torch_release':
        #     version_query = {
        #         'framework': 'paddle',
        #         'place': origin_data['place'],  # cpu和gpu性能差异较大,所以将place查询优先级提升
        #         'version': torch_release_version,
        #     }
        #     torch_release_query = dict(query, **version_query)
        #     data_list = await Job.aio_filter_details(limit=1, order_by='-create_time', **torch_release_query)
        #     if bool(data_list) is False:  # 如果查不到符合所有条件的数据，就使用符合version_query条件的数据
        #         data_tmp = await Job.aio_filter_details(limit=1, order_by='-create_time', **version_query)
        #         if bool(data_tmp) is False:
        #             raise HTTP400Error("数据库中，相关基线数据缺失")
        #         else:
        #             data = data_tmp[0]
        #     else:
        #         data = data_list[0]
        else:
            raise HTTP400Error("数据库中，相关基线数据缺失")

        data["create_time"] = str(data.get("create_time"))
        data["update_time"] = str(data.get("update_time"))
        return 1, data
