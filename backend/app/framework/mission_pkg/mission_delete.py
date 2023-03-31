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
from app.framework.dispatcher import Dispatcher
from app.framework.config.service_url import COMPILE_SERVICE
import requests
from app.framework.utils.callback import get_job_status



class MissionDelete(MABaseView):
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
            "result": "手动删除任务",
            "update_time": datetime.now(),
            "is_deleted": 1,
        }
        res = await Mission.aio_update(data, {"id": mission_id})
        if res == 0:
            raise HTTP400Error
        else:
            return "删除成功"

