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
from framework.utils.callback import get_job_status
from framework.utils.xly import pipeline_cancel



class MissionCancel(MABaseView):
    """
    手动标记任务失败
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        快速失败
        """
        mission_id = kwargs.get("id")
        # 获取效率云任务id
        data = await Mission.aio_filter_details(limit=1, id=mission_id)
        if len(data) != 1:
            raise HTTP400Error("任务取消失败,没有找到指定任务，请排查任务ID")
        description = data[0].get("description", None)
        if description is None:
            raise HTTP400Error("任务取消失败,没有找到指定效率云任务，请排查效率云任务ID（description）")
        res = pipeline_cancel(description)
        if not res:
            raise HTTP400Error("任务取消失败")
        data = {
            "result": "手动取消任务",
            "update_time": datetime.now(),
            "status": "error",
        }
        res = await Mission.aio_update(data, {"id": mission_id})
        if res == 0:
            raise HTTP400Error
        else:
            # get jid
            mission = await Mission.aio_get_object(id=mission_id)
            job = await Job.aio_get_object(id=mission["jid"])
            await get_job_status(job["id"], json.loads(job["mission"]))




