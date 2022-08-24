# !/usr/bin/env python3
# encoding: utf-8
"""
定义ce 的taks表
"""
import asyncio
import os
import sys
import time

import sqlalchemy as sa
from libs.mysql.db import BaseModel, BaseModelMixin, db_engines
from libs.mysql.schema import Column
from sqlalchemy import (VARCHAR, BigInteger, Boolean, Column, Float, Integer,
                        Text)
from utils.md5 import get_md5


class PubishTaskBuilds(BaseModel, BaseModelMixin):
    """
    定义tasks任务的执行是的表结构
    """
    __tablename__ = 'publish_task_builds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tid = Column(Integer, comment="关联任务表中的任务id") # 改栏的取值为ce_tasks表中的id,将任务信息与编译信息
    repo = Column(VARCHAR(50), comment='repo name') # 这里默认是paddle
    commit_id = Column(VARCHAR(100), comment= '提交版本号') # 任务回归覆盖的commit id
    commit_time = Column(Integer, comment="覆盖paddle的commit提交的时间，单位秒")
    build_time = Column(Integer, comment="任务开始执行时间戳，单位秒") # 任务开始执行时间
    tag = Column(VARCHAR(50), comment="版本号") # 任务覆盖的paddle的版本号
    build_id = Column(VARCHAR(50), comment="任务序列号") # xly:AGILE_PIPELINE_BUILD_ID; tc:%teamcity.build.id%
    job_id = Column(VARCHAR(50), comment="step id") # xly:AGILE_JOB_BUILD_ID; tc:不需要改参数，但是为了占位，可以传递%teamcity.build.step.name%
    test_step = Column(Integer, comment="任务执行的阶段")
    status = Column(VARCHAR(20), comment="任务的直接结果") # 任务的状态： Doing、Passed、Failed
    created = Column(Integer, comment="任务本次构建的开始时间，单位秒") # 开始构建的时间
    updated = Column(Integer, comment="本条记录的修改时间，单位秒") # 本记录的更新时间

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'

    @classmethod
    async def create_or_update_build(cls, tid, build_id, **validated_data):
        record = await cls.aio_get_object(
            **{"tid": tid, "build_id": build_id}
        )
        if record:
            row_id = record.id
            await cls.aio_update(
                validated_data=validated_data, params_data={"id": row_id}
            )
        else:
            await cls.aio_insert(validated_data={
                "tid": tid,
                "repo": validated_data.get("repo"),
                "tag": validated_data.get("tag"),
                "commit_id": validated_data.get("commit_id"),
                "commit_time": validated_data.get("commit_time"),
                "build_time": validated_data.get("build_time") or int(time.time()),
                "build_id": build_id,
                "job_id": validated_data.get("job_id"),
                "test_step": validated_data.get("test_step"),
                "status": validated_data.get("status")
                })
