#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile
from exception import HTTP400Error
from datetime import datetime
from framework.config.service_url import Local
import requests


class Dispatcher(object):
    """
    调度器
    """
    @classmethod
    def request_mission(self, module, id, env, wheel):
        # todo: 请求任务 任务环境，编译内容，发送请求给效率云
        if module == "api":
            data = {"id": id, "env": env, "wheel": wheel}
            res = requests.post(Local.API_FUNCTION, json=data)
            if res.json().get("code") == 200:
                return True
            else:
                return False
        else:
            # todo: 其他策略
            raise HTTP400Error

    @classmethod
    async def dispatch_missions(self, job):
        """
        任务分发器
        """
        # todo: 并行触发服务，初始化对应的服务数据

        mission = json.loads(job.get("mission"))
        res = await Compile.aio_get_object(order_by=None, group_by=None, id=job.get("compile"))
        wheel = res["wheel"]
        env = res["env"]
        retry_time = 5
        for k, v in mission.items():
            # if v is not None:
            #     continue
            retry = 0
            data = {"jid": job.get("id"),
                    "status": "init",
                    "module": k,
                    "create_time": datetime.now(),
                    "update_time": datetime.now()},
            res = await Mission.aio_insert(data)
            if res[0] == 0:
                raise HTTP400Error
            id = res[1]
            mission[k] = id

            while(retry < retry_time):
                res = self.request_mission(k, id, env, wheel)
                if res:
                    # todo:初始化任务
                    await Mission.aio_update({"status": "running"}, {"id":id})
                    break
                else:
                    retry += 1
        await Job.aio_update({"mission": str(json.dumps(mission))}, {"id":job.get("id")})


