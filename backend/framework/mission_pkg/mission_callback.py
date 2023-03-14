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
from framework.config.status import MissionStatus
from framework.dispatcher import Dispatcher
from framework.utils.callback import get_job_status
import requests
from framework.config.status import ERROR_MSG


class MissionCallback(MABaseView):
    """
    mission 回调函数
    """
    #Todo： 效率云回调内容不明确，使用MAPPING映射，防止后面的改动太大
    STATUS_MAPPING = {
        "PENDING": "running",
        "RUNNING": "running",
        "SUCC": "done",
        "FAIL": "fail",
    }
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        mission 回调函数
        """
        id = kwargs.get("id", None)
        pipelineid = kwargs.get("AGILE_PIPELINE_BUILD_ID")
        kwargs["update_time"] = datetime.now()
        #  Todo：解析数据 self.request.headers.get() 等对齐数据结构就OK「
        TRIGGER_TYPE = self.request.headers.get("TRIGGER_TYPE", None)
        if id is not None:
            res = await Mission.aio_update(kwargs, {"id": id})
        elif TRIGGER_TYPE == "STATUS":
            # Todo： 因为回调内容不明确，所以先做兼容性写法
            exit_code = self.request.headers.get("JOB_EXIT_CODE", None)
            if exit_code is None:
                exit_code = kwargs.get("JOB_EXIT_CODE")
            # Todo: TRIGGER_TYPE 必须是 STATUS才认定为自动回调
            if exit_code == "0":
                # Todo: 对齐成功回调的数据内容，解析映射数据库字段，入库
                data = {
                    "status": self.STATUS_MAPPING.get(self.request.headers.get("BUILD_STATUS")),
                    "result": kwargs.get("result"),
                    "allure_report": kwargs.get("allure_report")
                }
            else:
                # Todo: 根据退出码赋值
                data = {
                    "status": "error",
                    "result": ERROR_MSG.get(exit_code),
                }
            res = await Mission.aio_update(data, {"description": pipelineid})
        else:
            raise HTTP400Error("非正常回调请求，通过TRIGGER_TYPE判断非自动触发回调")
        if res == 0:
            raise HTTP400Error("回调数据有问题")
        # get jid
        mission = await Mission.aio_get_object(id=id)
        job = await Job.aio_get_object(id=mission["jid"])
        await get_job_status(job["id"], json.loads(job["mission"]))
        # jid = jid["jid"]






