# !/usr/bin/env python3
# encoding: utf-8
"""
定义ce 的taks表
"""
import asyncio
import os
import sys

import sqlalchemy as sa
from libs.mysql.db import BaseModel, BaseModelMixin, db_engines
from libs.mysql.schema import Column
from sqlalchemy import VARCHAR, BigInteger, Boolean, Column, Float, Integer, Text
from utils.md5 import get_md5


class XlyBuild(BaseModel, BaseModelMixin):
    """
    定义tasks任务的执行是的表结构
    """
    __tablename__ = 'xly_run_info'
    build_id = Column(Integer, comment="构建流水线id对应效率云AGILE_PIPELINE_BUILD_ID") 
    job_id = Column(Integer, primary_key=True, comment="构建任务id对应效率云AGILE_JOB_BUILD_ID") 
    exit_code = Column(Integer, comment="任务退出码")
    status = Column(VARCHAR(20), comment="任务状态对应效率云BUILD_STATUS")
    fail_reason = Column(VARCHAR(20), comment="任务标注失败原因")
    bein_time = Column(Integer, comment="任务开始调度时间单位秒") 
    run_time = Column(Integer, comment="任务开始执行时间单位秒") 
    end_time = Column(Integer, comment="任务结束执行时间单位秒") 
    conf_id = Column(Integer, comment="任务配置id对应效率云AGILE_PIPELINE_CONF_ID") 
    created = Column(Integer, comment="任务本次构建的开始时间，单位秒") # 开始构建的时间
    updated = Column(Integer, comment="本条记录的修改时间，单位秒") # 本记录的更新时间

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
