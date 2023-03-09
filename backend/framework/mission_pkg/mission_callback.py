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
from framework.config.status import MissionStatus
from framework.dispatcher import Dispatcher
from framework.utils.callback import get_job_status
import requests


class MissionCallback(MABaseView):
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
        pipelineid = kwargs.get("AGILE_PIPELINE_BUILD_ID")
        kwargs["update_time"] = datetime.now()
        #  Todo：解析数据 self.request.header.get() 等大佬给数据结构
        if id is not None:
            res = await Mission.aio_update(kwargs, {"id": id})
        else:
            res = await Mission.aio_update(kwargs, {"description": pipelineid})
        if res == 0:
            raise HTTP400Error("回调数据有问题")
        # get jid
        mission = await Mission.aio_get_object(id=id)
        job = await Job.aio_get_object(id=mission["jid"])
        await get_job_status(job["id"], json.loads(job["mission"]))
        # jid = jid["jid"]






