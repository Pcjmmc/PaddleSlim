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
from framework.config.status import MissonStatus
from framework.dispatcher import Dispatcher
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
        status = kwargs.get("status")
        result = kwargs.get("result")
        bos_url = kwargs.get("bos_url")
        allure_report = kwargs.get("report")
        data = {
            "id": id,
            "status": status,
            "result": result,
            "bos_url": bos_url,
            "allure_report": allure_report,
            "update_time": datetime.now()
        }
        res = await Mission.aio_update(data, {"id": id})
        if res == 0:
            raise HTTP400Error
        # get jid
        mission = await Mission.aio_get_object(id=id)
        job = await Job.aio_get_object(id=mission["jid"])
        await self.get_job_status(job["id"], json.loads(job["mission"]))
        # jid = jid["jid"]


    async def get_job_status(self, jid,missions: dict):
        """
        查看job的所有任务状态，更新状态
        """
        result_list = []
        for v in missions.values():
            mission = await Mission.aio_get_object(id=v)
            result_list.append(mission["status"])
        # print(result_list)
        # 如果 有 running 在里面，不修改状态。
        if MissonStatus.RUNNING in result_list:
            pass
        # 如果没有running在里面，如果有error，修改状态为error
        else:
            if MissonStatus.ERROR in result_list:
                res = await Job.aio_update({"status": MissonStatus.ERROR},{"id": jid})
            else:
                res = await Job.aio_update({"status": MissonStatus.DONE}, {"id": jid})
            if res == 0:
                raise HTTP400Error





