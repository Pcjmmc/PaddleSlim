#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile, FeedBack
from exception import HTTP400Error
from datetime import datetime
import requests


class FeedBackView(MABaseView):
    """
    云燊编译系统调用，构造缓存数据库
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        feedback
        """
        # 构造入库数据
        data = {}
        data["uid"] = self._cookies.get("userid", 0)
        data["username"] = self._cookies.get("username", 0)
        data["content"] = kwargs.get("content")
        data["star"] = kwargs.get("star")
        data["create_time"] = datetime.now()
        data["update_time"] = datetime.now()
        res = await FeedBack.aio_insert(data)
        if res[0] == 0:
            raise HTTP400Error("数据写入失败")
        else:
            return "数据写入成功"


