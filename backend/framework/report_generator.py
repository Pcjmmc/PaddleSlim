#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python


"""
下载报告
配置 allure路径
生成文件，放到指定的位置
将生成地址和对应任务关联起来
"""

import asyncio
import json
import os

import wget

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile
from exception import HTTP400Error
from datetime import datetime
from framework.dispatcher import Dispatcher
import requests
import random
import time
from framework.config.status import ERROR_600, ERROR_601, ERROR_602
from framework.config.service_url import REPORT_SOURCE_NAME, WWW_DIR, SOURCE_DIR, REPORT_SERVER


class ReportGenerator(MABaseView):
    """
    mission 回调函数
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        下载报告
        配置 allure路径
        生成文件，放到指定的位置
        将生成地址和对应任务关联起来
        """
        # 下载报告
        mission_id = kwargs.get("id")
        url = kwargs.get("bos_url")

        if os.path.exists(REPORT_SOURCE_NAME):
            os.remove(REPORT_SOURCE_NAME)
        wget.download(url,out=REPORT_SOURCE_NAME)
        filename = str(random.randint(0, 33)) + str(int(time.time())) + "_id_" + mission_id
        # for test
        WWW_DIR = "./test/"
        SOURCE_DIR = "./test/hahaha/"
        # end test
        file_path = WWW_DIR + filename
        print("report file path = {}".format(file_path))
        res = os.system("mkdir -p {} && tar xf ./pts_report.tar -C {} --strip-components 1".format(file_path, file_path))
        if res != 0:
            return HTTP400Error(ERROR_600)

        # 生成allure html文件
        res = os.system("./test/allure/bin/allure generate {} -o {} --clean".format(file_path, SOURCE_DIR + filename))
        if res != 0:
            return HTTP400Error(ERROR_601)

        # 入库
        report_url = REPORT_SERVER + filename
        res = await Mission.aio_update({"allure_report": report_url}, {"id": mission_id})
        if res == 0:
            raise HTTP400Error(ERROR_602)
        
        return {"allure_report": report_url}





