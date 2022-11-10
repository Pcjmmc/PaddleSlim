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
import requests


class CompileDatabase(MABaseView):
    """
    云燊编译系统调用，构造缓存数据库
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        云燊编译系统调用，构造缓存数据库
        """
        # {"type": "wheel", "value": "https://xly-devops.bj.bcebos.com/paddlepaddle_gpu-0.0.0-cp37-cp37m-linux_x86_64.whl", "python": "python3.7", "cuda": "v11.2", "os": "Linux", "branch": "develop"}
        env = dict()
        env["type"] = kwargs.get("pd_type")
        env["value"] = kwargs.get("value")
        env["branch"] = kwargs.get("branch")
        env["python"] = kwargs.get("python")
        env["cuda"] = kwargs.get("cuda")
        env["os"] = kwargs.get("os")
        # 构造入库数据
        data = dict()
        data["jid"] = 0
        data["uid"] = 0
        data["status"] = "done"
        data["env"] = str(env)
        data["create_time"] = datetime.now()
        data["update_time"] = datetime.now()
        data = dict(data, **kwargs)

        res = await Compile.aio_insert(data)
        if res[0] == 0:
            raise HTTP400Error("数据写入失败")
        else:
            return "数据写入成功"


