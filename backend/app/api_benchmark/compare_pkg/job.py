#!/bin/env python3
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

class GetJob(MABaseView):
    """
    查看version
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        cuda = kwargs.get("cuda")
        os = kwargs.get("os")
        version = kwargs.get("version")
        place = kwargs.get("place")
        query_dict = {}
        if cuda != "all":
            query_dict["cuda"] = cuda
        if os != "all":
            query_dict["system"] = os
        if version != "all":
            query_dict["version"] = version
        if place != "all":
            query_dict["place"] = place
        print(query_dict)
        data =  await Job.aio_filter_details(need_all=True, status="done", mode="schedule", **query_dict)
        res = []
        for i in data:
            temp = {
                "id": i["id"],
                "framework": i["framework"],
                "commit": i["commit"],
                "create_time": str(i["create_time"]),
                "snapshot": i["snapshot"]
            }
            res.append(temp)
        return len(data), res

