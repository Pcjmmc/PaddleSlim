#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
性能对比工具
"""
import asyncio
import json
from datetime import datetime
import requests
from exception import HTTP400Error

from views.base_view import MABaseView
from models.fd_benchmark import Job, Mission, Case


class TwoJobsMissionsId(MABaseView):
    """
    输入两个job id，返回dict(....)
    """

    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        job0_id = kwargs.get('id0')
        job0_list = await Job.aio_filter_details(limit=1, id=job0_id)
        job0 = job0_list[0]
        job0_mission = json.loads(job0['mission'])

        job1_id = kwargs.get('id1')
        job1_list = await Job.aio_filter_details(limit=1, id=job1_id)
        job1 = job1_list[0]
        job1_mission = json.loads(job1['mission'])

        common_keys = list(job0_mission.keys() & job1_mission.keys())

        mission_dict = {}
        # mission_dict = {"x86": [33, 22], "gpu": [32, 20], "arm": [11, 2]}
        for key in common_keys:
            mission_dict[key] = [job0_mission[key], job1_mission[key]]

        return len(common_keys), mission_dict
