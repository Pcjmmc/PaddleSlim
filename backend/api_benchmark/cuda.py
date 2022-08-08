#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

import asyncio
import json

from views.base_view import MABaseView
from models.api_benchmark import Settings
from exception import HTTP400Error
from datetime import datetime
import requests

class GetCuda(MABaseView):
    """
    查看Cuda
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        data =  await Settings.aio_get_object(option="cuda")
        res = data[1].split(",")
        return len(res), res

