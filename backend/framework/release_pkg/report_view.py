#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

import asyncio
import json

from views.base_view import MABaseView
from models.framework import ReleaseDailySettings, ReleaseDailyContent
from exception import HTTP400Error
from datetime import datetime
from framework.dispatcher import Dispatcher
import requests


class ReportView(MABaseView):
    """
    天级报告展示
    """
    async def get(self, **kwargs):
        """
        get
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        获取数据
        """
        settings = await self.get_report_settings()
        data = {"settings": settings, "content": []}
        for setting in settings:
            module_id = setting["id"]
            res = await ReleaseDailyContent.aio_filter_details(order_by="-create_time",
                                                               module_id=module_id, version=self._cookies.get("ver"))
            if len(res) == 0:
                continue
            else:
                res[0]["create_time"] = str(res[0]["create_time"] )
                data["content"].append(res[0])
        # print(data)
        return len(settings), data


    async def get_report_settings(self):
        """
        获取看板配置信息
        """
        return await ReleaseDailySettings.aio_filter_details(need_all=True)

