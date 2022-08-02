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


class DispatcherView(MABaseView):
    """
    调度器
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        compileid  or jid
        """
        id = kwargs.get("id")
        jid = kwargs.get("jid")
        if id is None and jid is None:
            raise HTTP400Error
        if jid is not None:
            res = await Job.aio_get_object(order_by=None, group_by=None, id=jid)
            await Dispatcher.dispatch_missions(res)
        else:
            jid = await Compile.aio_get_object(order_by=None, group_by=None, id=id).get("jid")
            res = await Job.aio_get_object(order_by=None, group_by=None, id=jid)



