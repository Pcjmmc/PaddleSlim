#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
首页性能对比
"""

import asyncio
import json

from views.base_view import MABaseView
from models.api_benchmark import Job, Case, Settings
from exception import HTTP400Error
from datetime import datetime
import requests


class BaseCompare(MABaseView):
    """
    任务初始化
    """

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        计算逻辑
        """
        my_job_id = kwargs.get('id')

        my_job_list = await Job.aio_filter_details(limit=1, id=my_job_id)
        my_job = my_job_list[0]
        my_commit = my_job['commit']
        my_wheel_link = my_job['wheel_link']
        my_place = my_job['place']
        my_cuda = my_job['cuda']
        my_python = my_job['python']
        my_create_time = my_job['create_time']

        develop = await Job.aio_filter_details(limit=1, order_by='-create_time', routine=1)
        latest_develop = develop[0]
        dev_id = latest_develop['id']
        latest_commit = latest_develop['commit']
        latest_wheel_link = latest_develop['wheel_link']
        latest_place = latest_develop['place']
        latest_cuda = latest_develop['cuda']
        latest_python = latest_develop['python']
        latest_create_time = latest_develop['create_time']

        data1 = await Case.aio_filter_details(need_all=True, jid=my_job_id)
        data2 = await Case.aio_filter_details(need_all=True, jid=dev_id)

        good = 0
        same = 0
        bad = 0
        res = []
        out = []
        # todo: 数据预处理
        res1 = {}
        res2 = {}
        for i in data1:
            res1[i["case_name"]] = i
        for i in data2:
            res2[i["case_name"]] = i
        for i in data1:
            case_name = i.get("case_name")
            temp = {
                "case_name": case_name,
                "api": i.get("api"),
                "my_job": dict(),
                "latest": dict(),
                "compare": dict()
            }
            if case_name not in res2.keys():
                continue
                # temp = {
                #     "case_name": case_name,
                #     "api": i.get("api"),
                #     "baseline": {
                #         "forward": float(json.loads(i.get("result")).get("forward")),
                #         "backward": float(json.loads(i.get("result")).get("backward")),
                #         "total": float(json.loads(i.get("result")).get("total")),
                #     },
                #     "latest": None,
                #     "compare": None,
                # }
            else:
                j = res2.get(case_name)
                forward_v1 = float(json.loads(i.get("result")).get("forward"))
                backward_v1 = float(json.loads(i.get("result")).get("backward"))
                total_v1 = float(json.loads(i.get("result")).get("total"))
                forward_v2 = float(json.loads(j.get("result")).get("forward"))
                backward_v2 = float(json.loads(j.get("result")).get("backward"))
                total_v2 = float(json.loads(j.get("result")).get("total"))
                if forward_v1 > forward_v2:
                    forward = (forward_v1 / forward_v2) * -1
                else:
                    forward = forward_v2 / forward_v1
                # 判断除数不能为0
                if backward_v1 == 0 or backward_v2 == 0:
                    backward = 0
                else:
                    if backward_v1 > backward_v2:
                        backward = (backward_v1 / backward_v2) * -1
                    else:
                        backward = backward_v2 / backward_v1
                if total_v1 > total_v2:
                    total = (total_v1 / total_v2) * -1
                else:
                    total = total_v2 / total_v1

                if total < -1.15:
                    bad += 1
                elif -1.15 < total < 1.15:
                    same += 1
                else:
                    good += 1

                temp = {
                    "case_name": case_name,
                    "api": i.get("api"),
                    "my_job": {
                        "forward": forward_v1,
                        "backward": backward_v1,
                        "total": total_v1,
                    },
                    "latest": {
                        "forward": forward_v2,
                        "backward": backward_v2,
                        "total": total_v2,
                    },
                    "compare": {
                        "forward": forward,
                        "backward": backward,
                        "total": total,
                    }
                }
            res.append(temp)
        summary = {}
        summary['good'] = str(good)
        summary['same'] = str(same)
        summary['bad'] = str(bad)
        out_tmp = {
            'my_job': {
                'commit': my_commit,
                'wheel_link': my_wheel_link,
                'place': my_place,
                'cuda': my_cuda,
                'python': my_python,
                'create_time': str(my_create_time),
            },
            'latest': {
                'commit': latest_commit,
                'wheel_link': latest_wheel_link,
                'place': latest_place,
                'cuda': latest_cuda,
                'python': latest_python,
                'create_time': str(latest_create_time),
            },
            'compare': res,
            'summary': summary,
        }
        out.append(out_tmp)
        return out
