#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

from views.base_view import MABaseView
from models.framework import Job
from exception import HTTP400Error
from datetime import datetime


class JobDelete(MABaseView):
    """
    手动标记任务失败
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        快速失败
        """
        job_id = kwargs.get("id")
        data = {
            "update_time": datetime.now(),
            "is_deleted": 1,
        }
        res = await Job.aio_update(data, {"id": job_id})
        if res == 0:
            raise HTTP400Error
        else:
            return "删除成功"


