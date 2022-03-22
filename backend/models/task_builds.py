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
    duration = Column(Integer, comment="任务本次的执行时长，单位秒") # 执行时长，单位秒
    created = Column(Integer, comment="任务本次构建的开始时间，单位秒") # 开始构建的时间
    updated = Column(Integer, comment="本条记录的修改时间，单位秒") # 本记录的更新时间

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'

    @classmethod
    async def create_or_update_build(cls, tid, build_id, validated_data={}):
        record = await cls.aio_get_object(
            **{"tid": tid, "build_id": build_id}
        )
        if record:
            row_id = record.id
            new_status = validated_data.get("status")
            new_exit_code = validated_data.get("exit_code")
            new_job_id = validated_data.get("job_id")
            origin_exit = record.exit_code
            if new_status == "Failed" or (new_exit_code and str(new_exit_code) != '0'):
                # 如果本次是失败才修改，成功就保留原来的状态
                if not origin_exit or str(origin_exit) == '0':
                    exit_code_list = list()
                else:
                    origin_exit = str(origin_exit)
                    exit_code_list = origin_exit.split(",")
                if new_exit_code:
                    exit_code_list.append(str(new_exit_code))
                # 去重复
                exit_code_list = [item for item in exit_code_list if item]
                exit_code_list = list(set(exit_code_list))
                exit_code = ",".join(exit_code_list)
                status = new_status
            else:
                # 保留原来的状态
                status = record.status if record.status else new_status
                # 如果原来的退出码空着，则完善下，不空就保留原来的
                exit_code = origin_exit if record.status != new_status else new_exit_code

            
            update_params = {
                "status": status,
                "exit_code": exit_code,
                "left_time": validated_data.get("left_time") or record.left_time,
                "duration": validated_data.get("duration") or record.duration
            }
            # 追加job id
            if new_job_id:
                job_id_list = str(record.job_id).split(",") if record.job_id is not None else list()
                job_id_list.append(str(new_job_id))
                job_id_list = [item for item in job_id_list if item]
                job_id_list = list(set(job_id_list))
                update_params["job_id"] = ",".join(job_id_list)

            # 可以更新的字段
            await cls.aio_update(
                validated_data=update_params,
                params_data={"id": row_id}
            )
        else: 
            await cls.aio_insert(validated_data={
                "tid": tid,
                "repo": validated_data.get("repo"),
                "branch": validated_data.get("branch"),
                "commit_id": validated_data.get("commit_id"),
                "commit_time": validated_data.get("commit_time"),
                "build_time": validated_data.get("build_time"),
                "build_id": build_id,
                "job_id": validated_data.get("job_id"),
                "created": validated_data.get("created"),
                "duration": validated_data.get("duration"),
                "status": validated_data.get("status"),
                "exit_code": validated_data.get("exit_code")
            })
