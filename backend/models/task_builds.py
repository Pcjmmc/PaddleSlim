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


class CeTaskBuilds(BaseModel, BaseModelMixin):
    """
    定义tasks任务的执行是的表结构
    """
    __tablename__ = 'ce_task_builds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tid = Column(Integer, comment="关联任务表中的任务id") # 改栏的取值为ce_tasks表中的id,将任务信息与编译信息
    repo = Column(VARCHAR(50), comment='repo name') # 这里默认是paddle
    commit_id = Column(VARCHAR(100), comment= '提交版本号') # 任务回归覆盖的commit id
    commit_time = Column(Integer, comment="覆盖paddle的commit提交的时间，单位秒")
    build_time = Column(Integer, comment="编包时间，单位秒") # 上游任务开始编包的时间
    branch = Column(VARCHAR(50), comment="提交分支") # 任务覆盖的分支信息
    build_id = Column(VARCHAR(50), comment="任务序列号") # xly:AGILE_PIPELINE_BUILD_ID; tc:%teamcity.build.id%
    job_id = Column(VARCHAR(50), comment="step id") # xly:AGILE_JOB_BUILD_ID; tc:不需要改参数，但是为了占位，可以传递%teamcity.build.step.name%
    status = Column(VARCHAR(20), comment="任务的直接结果") # 任务的状态： runnig、Passed、Failed
    left_time = Column(Integer, comment="任务本次执行的剩余时间，单位秒") # 当任务状态是running的时候，需要给出大概需要多久能执行完
    exit_code = Column(VARCHAR(200), comment="任务退出码") # 任务的退出码, 约定任务的详细失败原因；多个以英文逗号分割
    created = Column(Integer, comment="任务本次构建的开始时间，单位秒") # 开始构建的时间
    updated = Column(Integer, comment="本条记录的修改时间，单位秒") # 本记录的更新时间

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'