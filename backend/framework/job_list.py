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

class JobList(MABaseView):
    """
    任务初始化
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            data =  await Job.aio_get_object(order_by=None, group_by=None, id=id)
            mission = dict()

            check_complete = True

            for k,v in json.loads(data["mission"]).items():
                res = await Mission.aio_get_object(order_by=None, group_by=None, id=v)
                mission[k] = {"id": v, "status": res["status"], "result": res["result"]}
                if res["status"] != "done":
                    check_complete = False
            if check_complete and data["status"] != "done":
                await Job.aio_update({"status": "done", "update_time": datetime.now()}, {"id": id})
                data = await Job.aio_get_object(order_by=None, group_by=None, id=id)

            res_data = {
                "id": data["id"],
                "status": data["status"],
                "mission": mission
            }
            return 1, res_data
        else:
            page_index = kwargs.get("page_index")
            limit = kwargs.get("limit")
            data = await Job.aio_filter_details(page_index=page_index, limit=limit, order_by="-id")
            for d in data:
                d["create_time"] = str(d["create_time"])
                d["update_time"] = str(d["update_time"])
                check_complete = True
                check_error = True
                mission = dict()
                for k, v in json.loads(d["mission"]).items():
                    res = await Mission.aio_get_object(order_by=None, group_by=None, id=v)
                    if res is None:
                        continue
                    mission[k] = {"id": v, "status": res["status"], "result": res["result"]}
                    if res["status"] != "done":
                        check_complete = False
                    if res["status"] == "running" or res["status"] ==  "init":
                        check_error = False
                if check_complete:
                    await Job.aio_update({"status": "done", "update_time": datetime.now()}, {"id": d["id"]})
                if check_error:
                    await Job.aio_update({"status": "error", "update_time": datetime.now()}, {"id": d["id"]})
                d["mission_status"] = mission
            return len(data), data
