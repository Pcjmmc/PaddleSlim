#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile, Settings, ModuleSettings
from exception import HTTP400Error
from datetime import datetime
from framework.dispatcher import Dispatcher
from framework.config.service_url import COMPILE_SERVICE
import requests

class ModuleSettingsView(MABaseView):
    """
    任务初始化
    """

    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        settings =  await ModuleSettings.aio_filter_details(need_all=True)
        module_name = ["module_list", "module_mapping"]
        res = {}
        for i in settings:
            if i["option"] in module_name:
                res[i["option"]] = i["value"]
        return len(res), res
