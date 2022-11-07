#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
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
from framework.config.status import MissonStatus

class MissionFailed(MABaseView):
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
        data = {
            "status": "error",
            "update_time": datetime.now()
        }
        res = await Mission.aio_update(data, {"id": mission_id})
        if res == 0:
            raise HTTP400Error
        # get jid
        mission = await Mission.aio_get_object(id=mission_id)
        job = await Job.aio_get_object(id=mission["jid"])
        await self.get_job_status(job["id"], json.loads(job["mission"]))

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