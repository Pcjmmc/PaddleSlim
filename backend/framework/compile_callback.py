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
import requests


class CompileCallback(MABaseView):
    """
    mission 回调函数
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        mission 回调函数
        """
        id = kwargs.get("id")
        status = kwargs.get("status")
        kwargs["update_time"] = datetime.now()
        # todo:这里需要实现逻辑，如果失败了如何处理，成功了如何处理。
        if status == "done":
            await Compile.aio_update(kwargs, {"id": id})
            res = await Compile.aio_get_object(order_by=None, group_by=None, id=id)
            jid = res["jid"]
            # 请求下游服务
            res = await Job.aio_get_object(order_by=None, group_by=None, id=jid)
            await Dispatcher.dispatch_missions(res)
        else:
            await Compile.aio_update(kwargs, {"id": id})
            res = await Compile.aio_get_object(order_by=None, group_by=None, id=id)
            jid = res["jid"]
            await Job.aio_update({"status": "error", "update_time": datetime.now()}, {"id": jid})






