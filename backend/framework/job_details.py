#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile
from exception import HTTP400Error
from datetime import datetime
from framework.dispatcher import Dispatcher
from framework.config.service_url import COMPILE_SERVICE
import requests

class JobDetails(MABaseView):
    """
    任务初始化
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        id = kwargs.get("id")
        data =  await Job.aio_get_object(order_by=None, group_by=None, id=id)
        compile = await Compile.aio_get_object(id=data["compile"])
        mission = dict()
        for k, v in json.loads(data["mission"]).items():
            if v is None:
                mission[k] = v
                continue
            res = await Mission.aio_get_object(order_by=None, group_by=None, id=v, is_deleted=0)
            mission[k] = {"id": v, "status": res["status"], "result": res["result"],
                          "bos_url": res["bos_url"], "allure_report": res["allure_report"],
                          "description": res["description"], "create_time": str(res["create_time"]),
                          "update_time": str(res["update_time"]), }
        res_data = {
            "id": data["id"],
            "uid": data["uid"],
            "status": data["status"],
            "description": data["description"],
            "compile_id": data["compile"],
            "compile": {
                "status": compile["status"],
                "wheel": compile["wheel"],
                "env": compile["env"],
                "create_time": str(compile["create_time"]),
                "update_time": str(compile["update_time"]),
            },
            "mission": mission,
            "create_time": str(data["create_time"]),
            "update_time": str(data["update_time"]),
        }
        return 1, res_data

