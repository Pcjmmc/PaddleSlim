#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import json

from views.base_view import MABaseView
from models.framework import Job, Mission
from exception import HTTP400Error
from datetime import datetime
from app.framework.utils.callback import get_job_status

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
            "result": "手动标记失败",
            "update_time": datetime.now()
        }
        res = await Mission.aio_update(data, {"id": mission_id})
        if res == 0:
            raise HTTP400Error
        # get jid
        mission = await Mission.aio_get_object(id=mission_id)
        job = await Job.aio_get_object(id=mission["jid"])
        await get_job_status(job["id"], json.loads(job["mission"]))
