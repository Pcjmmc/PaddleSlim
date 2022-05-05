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


class CeCases(BaseModel, BaseModelMixin):
    """
    定义任务case结果的表结构
    """
    __tablename__ = 'ce_case_second_class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tid = Column(Integer, comment="关联任务表中的任务id") # ce_tasks表中的confid
    build_id = Column(VARCHAR(50), comment="任务序列号") # xly:AGILE_PIPELINE_BUILD_ID; tc:%teamcity.build.id%
    label = Column(VARCHAR(100), comment="二级分类名") #
    status = Column(VARCHAR(20), comment="任务的直接结果") # 任务的状态：Passed、Failed
    total = Column(Integer, comment="二级分类case总数")
    passed_num = Column(Integer, comment="二级分类成功的case数")
    failed_num = Column(Integer, comment="二级分类失败的case数")
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")


    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'

    @classmethod
    async def create_or_update_build(cls, tid, build_id, status, total, passed_num, failed_num, secondary_type):
        record = await cls.aio_get_object(
            **{"tid": tid, "build_id": build_id}
        )
        #任务存在直接删掉原来的记录&同时对应的mongodb record也需要删除
        if record:
            row_id = record.id
            await cls.aio_delete(
                params_data={"id": row_id}
            )
        await cls.aio_insert(validated_data={
            "tid": tid,
            "build_id": build_id,
            "status": status,
            "total": total,
            "label":secondary_type,
            "passed_num": passed_num,
            "failed_num": failed_num
            })
