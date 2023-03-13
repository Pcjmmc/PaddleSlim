#!/bin/env python
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


class MainCompare(MABaseView):
    """
    任务初始化
    """

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        计算逻辑
        """
        # baseline_id = 31
        baseline_set = await Settings.aio_filter_details(limit=1, option='baseline')

        baseline_id = json.loads(baseline_set[0]['value'])['cuda11.6']
        # print(baseline_id)

        baseline_list = await Job.aio_filter_details(limit=1, id=baseline_id)
        baseline = baseline_list[0]
        # print(baseline)
        baseline_ver = baseline['version']

        develop = await Job.aio_filter_details(limit=1, order_by='-create_time', routine=1)
        latest_develop = develop[0]
        dev_id = latest_develop['id']
        latest_commit = latest_develop['commit']
        latest_place = latest_develop['place']
        latest_create_time = latest_develop['create_time']

        data1 = await Case.aio_filter_details(need_all=True, jid=baseline_id)
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
                "baseline": dict(),
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
                if total_v1 > total_v2:  # baseline耗时更多
                    total = (total_v1 / total_v2) * -1
                else:  # latest耗时更多
                    total = total_v2 / total_v1

                if total < -1.15:
                    good += 1
                elif -1.15 < total < 1.15:
                    same += 1
                else:
                    bad += 1
                temp = {
                    "case_name": case_name,
                    "api": i.get("api"),
                    "baseline": {
                        "forward": forward_v1,
                        "backward": backward_v1,
                        "total": total_v1,
                    },
                    "latest":{
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
            'baseline': {'version': baseline_ver},
            'latest': {'commit': latest_commit, 'place': latest_place, 'create_time': str(latest_create_time)},
            'compare': res,
            'summary': summary,
        }
        out.append(out_tmp)
        return out
