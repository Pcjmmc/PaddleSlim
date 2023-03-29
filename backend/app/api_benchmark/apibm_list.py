#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
  * @file:  apibm_view.py
  * @author:  luozeyu01
  * @date  2023/2/24 11:17 AM
  * @brief
  *
  **************************************************************************/
"""
import asyncio
import json
import datetime


from views.base_view import MABaseView
from models.api_benchmark import Job
from utils.change_time import get_begin_and_time


from views.auth_view import AuthCheck

# DELETE when Release
SuperUser = ["1", "2", "7", "28", "13"]


class ApiBenchmarkList(MABaseView):
    """
    任务初始化
    """

    auth_class = AuthCheck

    def process_params(self, **kwargs):
        """
        对请求参数进行预处理
        """
        # >=
        if ( kwargs.get('begin_time') is not None ):
            kwargs["create_time__gte"] = kwargs.get('begin_time')
            kwargs.pop('begin_time')
        # < 
        if (kwargs.get('end_time') is not None):
            kwargs["create_time__lt"] = kwargs.get('end_time')
            kwargs.pop('end_time')
        # all in 
        if (kwargs.get("status") is None):
            kwargs['status__in'] = ["running",'done',"error","prepare"]
        # comment like
        if ( kwargs.get('comment') is not None):
            kwargs['comment__contains'] = "%" + kwargs.get('comment') + "%"
            kwargs.pop('comment')
        return kwargs

    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
      
        kwargs = self.process_params(**kwargs)
        userid = self._cookies.get("userid", 0)
        kwargs['uid'] = userid
        # print(kwargs)

        query = dict({"order_by": "-id"}, **kwargs)
        data = await Job.aio_filter_details(**query)
        count = await Job.aio_filter_count(**query)
        for d in data:
            d["create_time"] = str(d.get("create_time"))
            d["update_time"] = str(d.get("update_time"))
        return count, data
