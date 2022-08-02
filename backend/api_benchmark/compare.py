#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

from views.base_view import MABaseView
from models.api_benchmark import Job, Case
from exception import HTTP400Error
from datetime import datetime
import requests

class Compare(MABaseView):
    """
    任务初始化
    """


    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        计算逻辑
        """
        version1 = kwargs.get("version1")
        version2 = kwargs.get("version2")

        data1 = await Case.aio_filter_details(need_all=True, jid=version1)
        data2 = await Case.aio_filter_details(need_all=True, jid=version2)
        res = []

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
                "version1": dict(),
                "version2": dict(),
                "compare": dict()
            }
            if case_name not in res2.keys():
                continue
                # temp = {
                #     "case_name": case_name,
                #     "api": i.get("api"),
                #     "version1": {
                #         "forward": float(json.loads(i.get("result")).get("forward")),
                #         "backward": float(json.loads(i.get("result")).get("backward")),
                #         "total": float(json.loads(i.get("result")).get("total")),
                #     },
                #     "version2": None,
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
                if  forward_v1 > forward_v2:
                    forward = (forward_v1 / forward_v2) * -1
                else:
                    forward = forward_v2 / forward_v1

                if backward_v1 > backward_v2:
                    backward = (backward_v1 / backward_v2) * -1
                else:
                    backward = backward_v2 / backward_v1

                if total_v1 > total_v2:
                    total = (total_v1 / total_v2) * -1
                else:
                    total = total_v2 / total_v1
                temp = {
                    "case_name": case_name,
                    "api": i.get("api"),
                    "version1": {
                        "forward": forward_v1,
                        "backward": backward_v1,
                        "total": total_v1,
                    },
                    "version2":{
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
        return res
