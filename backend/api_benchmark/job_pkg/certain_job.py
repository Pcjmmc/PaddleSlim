#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  latest_routine_job.py
  * @author:  luozeyu01
  * @date  2023/3/21 2:46 PM
  * @brief 使用条件查询特定的任务
  *
  **************************************************************************/
"""
import asyncio
import json

from views.base_view import MABaseView
from models.api_benchmark import Job, Case
from exception import HTTP400Error
from datetime import datetime
import requests

class CertainJob(MABaseView):
    """
    查看version
    """
    def process_params(self, **kwargs):
        """
        对请求参数进行预处理
        """
        # >=
        query = {}
        if kwargs.get('begin_time') is not None:
            # kwargs["create_time__gte"] = kwargs.get('begin_time')
            # kwargs.pop('begin_time')
            query["create_time__gte"] = kwargs.get('begin_time')
        # <
        if kwargs.get('end_time') is not None:
            # kwargs["create_time__lt"] = kwargs.get('end_time')
            # kwargs.pop('end_time')
            query["create_time__lt"] = kwargs.get('end_time')
        # job done
        if kwargs.get("status") is None:
            # kwargs['status__in'] = ['done']
            # kwargs['status__in'] = ["running",'done',"error","prepare"]
            query['status__in'] = ['done']
        # comment like
        if kwargs.get('comment') is not None:
            # kwargs['comment__contains'] = "%" + kwargs.get('comment') + "%"
            # kwargs.pop('comment')
            query['comment__contains'] = "%" + kwargs.get('comment') + "%"
        if kwargs.get('commit') is not None:
            query["commit"] = kwargs.get("commit")

        if kwargs.get("framework") != "all":
            query["framework"] = kwargs.get("framework")
        if kwargs.get("cuda") != "all":
            query["cuda"] = kwargs.get("cuda")
        if kwargs.get("os") != "all":
            query["system"] = kwargs.get("os")
        if kwargs.get("version") != "all":
            query["version"] = kwargs.get("version")
        if kwargs.get("place") != "all":
            query["place"] = kwargs.get("place")

        return query

    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        query = self.process_params(**kwargs)
        query = dict({"order_by": "-id"}, **query)
        data =  await Job.aio_filter_details(need_all=True, **query)
        count = await Job.aio_filter_count(**query)

        for d in data:
            d["create_time"] = str(d.get("create_time"))
            d["update_time"] = str(d.get("update_time"))
        return count, data
