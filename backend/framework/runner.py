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
import os
import subprocess


class RunnerView(MABaseView):
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        id = kwargs.get("id")
        env = kwargs.get("env")
        wheel = kwargs.get("wheel")
        try:
            self.runner(id, env, wheel)
        except Exception as e:
            print(e)
            raise HTTP400Error

    def runner(self, id, env, wheel):
        # todo: 编写代码执行程序

        py_interpretor = json.loads(env).get("python")
        subprocess.Popen("cd test && bash ./test.sh {} {} {}".format(py_interpretor, wheel, id), shell=True)



