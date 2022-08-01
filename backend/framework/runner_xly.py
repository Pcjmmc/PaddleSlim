#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

import requests

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile
from exception import HTTP400Error
from datetime import datetime
from framework.utils.xly import XlyOpenApiRequest
import os
import subprocess


class RunnerXLY(MABaseView):
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        id = kwargs.get("id")
        wheel = kwargs.get("wheel")
        try:
            self.runner(id, wheel)
        except Exception as e:
            print(e)
            raise HTTP400Error

    def runner(self, id, wheel):
        # todo: 编写代码执行程序
        xly_agent = XlyOpenApiRequest()
        pipelineid = "23490"
        url_param = "pipelineId={}".format(pipelineid)
        # branch ciType commit 毛用没有
        params = {
            "id": id,
            "wheel": wheel,
        }
        data = {
            "branch": "develop",
            "ciType": "MERGE",
            "params": json.dumps(params)
        }
        data = json.dumps(data)
        url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipeline-builds?pipelineId={}".format(pipelineid)
        res = xly_agent.post_method(url, data, param=url_param)

        print(res.json())
