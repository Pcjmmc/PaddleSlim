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


class CompileInit(MABaseView):
    """
    mission 回调函数
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        mission 回调函数
        """
        data = dict()
        data["version"] = kwargs.get("value")
        data["uid"] = self._cookies.get("userid", 0)
        data["status"] = "running"
        data["description"] = kwargs.get("name")
        data["create_time"] = datetime.now()
        data["update_time"] = datetime.now()
        res = await Job.aio_insert(data)
        if res[0] == 0:
            raise HTTP400Error
        jid = res[1]
        pd_type = kwargs.get("type")
        value = kwargs.get("value")
        python = kwargs.get("python")
        cuda = kwargs.get("cuda")
        os = kwargs.get("os")
        branch = kwargs.get("branch")
        dist_type = bool(kwargs.get("dist_type"))
        cache = kwargs.get("cache", True)
        uid = self._cookies.get("userid", 0)
        await self.wheel_cache(jid, uid, pd_type, value, python, cuda, os, branch, dist_type, cache)
        return {"jid": jid}

    async def cache(self, query):
        """
        历史缓存查询命中
        """
        query = dict({"status": "done"}, **query)
        data = await Compile.aio_filter_details(need_all=False, **query)
        return data

    async def wheel_cache(self, jid, uid, pd_type, value, python, cuda=None, os=None, branch=None, dist_type="wheel", cache=True):
        """
        编译查询器,后续替换成云燊的服务
        wheel, version, pr, commit 四个编译类型任务，后三个走编译服务
        """
        data = dict()
        data["jid"] = jid
        data["status"] = "init"
        data["env"] = str(json.dumps({"type": pd_type,
                       "value": value,
                       "python": python,
                       "cuda": cuda,
                       "os": os,
                       "branch": branch}))
        data["pd_type"] = pd_type
        data["value"] = value
        data["python"] = python
        data["cuda"] = cuda
        data["os"] = os
        data["branch"] = branch
        data["uid"] = uid

        data["create_time"] = datetime.now()
        data["update_time"] = datetime.now()
        res = await Compile.aio_insert(data)
        if res[0] == 0:
            raise HTTP400Error("compile库初始化数据失败")
        res = await Job.aio_update({"compile": res[1]}, {"id": jid})
        if res == 0:
            raise HTTP400Error("Job库更新状态失败")
        # 编译服务
        compile_info = await Compile.aio_get_object(order_by=None, group_by=None, jid=jid)
        id = compile_info[0]
        data = {
            "id": id,
            "pd_type": pd_type,
            "value": value,
            "python": python,
            "cuda": cuda,
            "os": os,
            "branch": branch,
            "dist_type": dist_type,
        }

        # 缓存命中
        query = {"pd_type": pd_type,
                       "value": value,
                       "python": python,
                       "cuda": cuda,
                       "os": os,
                       "branch": branch}

        res = await self.cache(query)
        if len(res) != 0 and cache:
            # 命中缓存 走缓存逻辑
            wheel_path = res[0].get("wheel")
            await Compile.aio_update({"status": "done", "wheel": wheel_path, "update_time": datetime.now()}, {"id": id})
            await Job.aio_update({"status": "done", "update_time": datetime.now()}, {"id": jid})
        else:
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
                    raise HTTP400Error("Compile 库更新结果失败")
                res = await Job.aio_update({"status": "error"}, {"id": jid})
                if res == 0:
                    raise HTTP400Error("Job 库更新结果失败")
            else:
                query = dict()
                query["jid"] = jid
                data = dict()
                data["status"] = "running"
                data["update_time"] = datetime.now()
                res = await Compile.aio_update(data, query)
                if res == 0:
                    raise HTTP400Error("Compile 库更新编译状态失败")
