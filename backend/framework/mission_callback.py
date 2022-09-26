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
        data = {
            "id": id,
            "status": status,
            "result": result,
            "bos_url": bos_url,
            "update_time": datetime.now()
        }
        res = await Mission.aio_update(data, {"id": id})
        if res == 0:
            raise HTTP400Error




