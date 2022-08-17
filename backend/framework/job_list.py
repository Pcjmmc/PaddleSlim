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
            compile = await Compile.aio_get_object(id=data["compile"])
            # 编译失败
            if compile["status"] not in ["done", "running"]:
                await Job.aio_update({"status": "error", "update_time": datetime.now()}, {"id": id})
                data = await Job.aio_get_object(order_by=None, group_by=None, id=id)
                res_data = {
                    "id": data["id"],
                    "status": data["status"],
                    "compile": {
                        "status": compile["status"],
                        "wheel": compile["wheel"],
                        "env": compile["env"],
                        "create_time": str(compile["create_time"]),
                        "update_time": str(compile["update_time"]),
                    },
                    "mission": data["mission"],
                }
                return 1, res_data
            elif compile["status"] == "running":
                data = await Job.aio_get_object(order_by=None, group_by=None, id=id)
                res_data = {
                    "id": data["id"],
                    "status": data["status"],
                    "compile": {
                        "status": compile["status"],
                        "wheel": compile["wheel"],
                        "env": compile["env"],
                        "create_time": str(compile["create_time"]),
                        "update_time": str(compile["update_time"]),
                    },
                    "mission": data["mission"],
                }
                return 1, res_data
            else:
                check_complete = True
                check_error = True
                mission = dict()
                for k,v in json.loads(data["mission"]).items():
                    if v is None:
                        check_complete = False
                        check_error = False
                        mission[k] = v
                        continue
                    res = await Mission.aio_get_object(order_by=None, group_by=None, id=v)
                    mission[k] = {"id": v, "status": res["status"], "result": res["result"],
                                  "description": res["description"], "create_time": str(res["create_time"]),
                                  "update_time": str(res["update_time"]),}
                    if res["status"] != "done":
                        check_complete = False
                    if res["status"] in ["done", "init", "running"]:
                        check_error = False
                if check_complete and data["status"] == "running":
                    await Job.aio_update({"status": "done", "update_time": datetime.now()}, {"id": id})
                    data = await Job.aio_get_object(order_by=None, group_by=None, id=id)
                elif check_error and not check_complete and data["status"] == "running":
                    await Job.aio_update({"status": "error", "update_time": datetime.now()}, {"id": id})
                    data = await Job.aio_get_object(order_by=None, group_by=None, id=id)
                res_data = {
                    "id": data["id"],
                    "status": data["status"],
                    "compile": {
                        "status": compile["status"],
                        "wheel": compile["wheel"],
                        "env": compile["env"],
                        "create_time": str(compile["create_time"]),
                        "update_time": str(compile["update_time"]),
                    },
                    "mission": mission,
                }
                return 1, res_data
        else:
            # 只返回查询列表
            page_index = kwargs.get("page_index")
            limit = kwargs.get("limit")
            data = await Job.aio_filter_details(page_index=page_index, limit=limit, order_by="-id")
            total = await Job.aio_filter_count()
            for d in data:
                d["create_time"] = str(d.get("create_time"))
                d["update_time"] = str(d.get("update_time"))
            return total, data
