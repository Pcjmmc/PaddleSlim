#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
首页性能对比
"""

import asyncio
import json

from views.base_view import MABaseView
from models.fd_benchmark import Job, Mission, Case
from exception import HTTP400Error
from datetime import datetime
from app.fd_benchmark.compare.compare_tools import case_compare
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
        if int(kwargs.get('id')) < 1 or int(kwargs.get('id1')) < 1:
            raise HTTP400Error("对比任务id不可小于等于0")
        
        # print(kwargs)
        baseline_id = kwargs.get('id')
        latest_id = kwargs.get('id1')

        # baseline_mission_list = await Mission.aio_filter_details(limit=1, id=baseline_id)
        # baseline_mission = baseline_mission_list[0]

        # my_commit = baseline_mission['commit']
        # my_wheel_link = baseline_mission['wheel_link']
        # my_place = baseline_mission['place']
        # my_cuda = baseline_mission['cuda']
        # my_python = baseline_mission['python']
        # my_create_time = baseline_mission['create_time']

        # latest_mission_list = await Mission.aio_filter_details(limit=1, id=latest_id)
        # latest_mission = latest_mission_list[0]

        # latest_commit = latest_develop['commit']
        # latest_wheel_link = latest_develop['wheel_link']
        # latest_place = latest_develop['place']
        # latest_cuda = latest_develop['cuda']
        # latest_python = latest_develop['python']
        # latest_create_time = latest_develop['create_time']

        baseline_cases = await Case.aio_filter_details(need_all=True, jid=baseline_id)
        latest_cases = await Case.aio_filter_details(need_all=True, jid=latest_id)

        res = []

        for latest_case in latest_cases:
            tmp = {}
            backend = latest_case.get("backend")
            model = latest_case.get("model")

            baseline_case_list = await Case.aio_filter_details(need_all=True, jid=baseline_id,
                                                               backend=backend, model=model)

            if bool(baseline_case_list):
                baseline_case = baseline_case_list[0]

                latest_res = latest_case.get("result")
                baseline_res = baseline_case.get("result")

                latest_return, baseline_return, compare_return = case_compare(latest_res=latest_res,
                                                                              baseline_res=baseline_res)

                tmp["backend"] = backend
                tmp["model"] = model
                tmp["latest"] = latest_return
                tmp["baseline"] = baseline_return
                tmp["compare"] = compare_return

                res.append(tmp)
            else:
                continue

        return res
