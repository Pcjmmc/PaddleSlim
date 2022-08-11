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
from framework.dispatcher import Dispatcher
from framework.config.service_url import COMPILE_SERVICE
import requests

class JobInitView(MABaseView):
    """
    任务初始化
    """
    RETRY_TIME = 5
    def mission_analyse(self, data):
        """
        模块解析器
        todo： 解析策略
        """
        if not isinstance(data, list):
            raise HTTP400Error
        mission = dict()
        for i in data:
            mission[i] = None
        return str(json.dumps(mission))

    async def wheel_cache(self, jid, pd_type, value, python, cuda=None, os=None, branch=None):
        """
        编译查询器,后续替换成云燊的服务
        wheel, version, pr, commit 四个编译类型任务，后三个走编译服务
        """
        data = dict()
        data["jid"] = jid
        data["status"] = "running"
        data["env"] = str(json.dumps({"type": pd_type,
                       "value": value,
                       "python": python,
                       "cuda": cuda,
                       "os": os,
                       "branch": branch}))
        data["create_time"] = datetime.now()
        data["update_time"] = datetime.now()
        res = await Compile.aio_insert(data)
        if res[0] == 0:
            raise HTTP400Error
        res = await Job.aio_update({"compile": res[1]}, {"id": jid})
        if res == 0:
            raise HTTP400Error
        if pd_type == "wheel":
            query = dict()
            query["jid"] = jid
            data = dict()
            data["wheel"] = value
            data["status"] = "done"
            data["update_time"] = datetime.now()
            res = await Compile.aio_update(data, query)
            if res == 0:
                raise HTTP400Error
            # 请求下游服务
            res = await Job.aio_get_object(order_by=None, group_by=None, id=jid)
            await Dispatcher.dispatch_missions(res)
        else:
            # todo: 编译服务
            compile_info = await Compile.aio_get_object(order_by=None, group_by=None, jid=jid)
            id = compile_info[0]
            data = {
                "id": id,
                "pd_type": pd_type,
                "value": value,
                "python": python,
                "cuda": cuda,
                "os": os,
                "branch": branch
            }
            RETRY_TIME = 5
            retry = 0
            while (retry < RETRY_TIME):
                res = requests.post(COMPILE_SERVICE, json=data)
                if res.status_code != 200:
                    print(res.text)
                    retry += 1
                    continue
                else:
                    break
            if retry == RETRY_TIME:
                query = dict()
                query["jid"] = jid
                data = dict()
                data["status"] = "error"
                data["update_time"] = datetime.now()
                res = await Compile.aio_update(data, query)
                if res == 0:
                    raise HTTP400Error
                res = await Job.aio_update({"status": "error"}, {"id": jid})
                if res == 0:
                    raise HTTP400Error
            else:
                query = dict()
                query["jid"] = jid
                data = dict()
                data["status"] = "running"
                data["update_time"] = datetime.now()
                res = await Compile.aio_update(data, query)
                if res == 0:
                    raise HTTP400Error




    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        初始化任务，查缓存

        1. 任务解析器
        2. 初始化快照信息入库
        """
        data = dict()

        mission = kwargs.get("mission")
        data["mission"] = self.mission_analyse(mission)
        data["version"] = kwargs.get("value")
        data["status"] = "running"
        data["create_time"] = datetime.now()
        data["update_time"] = datetime.now()
        res = await Job.aio_insert(data)
        if res[0] == 0:
            raise HTTP400Error
        jid = res[1]

        # 启动缓存查询
        pd_type = kwargs.get("type")
        value = kwargs.get("value")
        python = kwargs.get("python")
        cuda = kwargs.get("cuda")
        os = kwargs.get("os")
        branch = kwargs.get("branch")
        await self.wheel_cache(jid, pd_type, value, python, cuda, os, branch)

        return {"jid": jid}



    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        id = kwargs.get("id")
        data =  await Job.aio_get_object(order_by=None, group_by=None, id=id)
        mission = dict()

        check_complete = True

        for k,v in json.loads(data["mission"]).items():
            res = await Mission.aio_get_object(order_by=None, group_by=None, id=v)
            mission[k] = {"id": v, "status": res["status"], "result": res["result"]}
            if res["status"] != "done":
                check_complete = False
        if check_complete:
            await Job.aio_update({"status": "done"}, {"id": id})
            data = await Job.aio_get_object(order_by=None, group_by=None, id=id)

        res_data = {
            "id": data["id"],
            "status": data["status"],
            "mission": mission
        }
        return 1, res_data
