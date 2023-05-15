# !/usr/bin/env python3
# encoding: utf-8
"""
定义二分查找任务的状态表格
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


class BinarySearchStatus(BaseModel, BaseModelMixin):
    """
    定义二分查找任务的执行表结构
    """
    __tablename__ = 'binary_search_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    xly_id = Column(VARCHAR(50), comment="效率云任务的id")  # 点击二分任务后所触发的xly任务id
    email = Column(VARCHAR(50), comment='当前用户的email账号')  # 在当前页面点击按钮的用户email
    xly_link = Column(VARCHAR(200), comment='xly任务链接')  # 点击二分任务后所触发的xly任务链接
    repo_name = Column(VARCHAR(50), comment="repo名")
    model_name = Column(VARCHAR(100), comment="model名")
    step_name = Column(VARCHAR(50), comment="step名")
    tag_name = Column(VARCHAR(50), comment="tag名")
    status = Column(VARCHAR(50), comment="xly任务执行过程中返回的状态信息")
    created = Column(Integer, comment="触发任务的时间")  # 触发任务的时间
    updated = Column(Integer, comment="本条记录的更新时间")  # 本记录的更新时间

    class Meta:
        """
        定义binary_search属于哪个库
        """
        app_label = 'paddle_quality'

    @classmethod
    async def create_or_update_build(cls, xly_id, **validated_data):
        record = await cls.aio_get_object(
            **{"xly_id": xly_id}
        )
        if record:
            row_id = record.id
            await cls.aio_update(
                validated_data=validated_data, params_data={"id": row_id}
            )
        else:
            await cls.aio_insert(validated_data={
                "xly_id": xly_id,
                "email": validated_data.get("email"),
                "xly_link": validated_data.get("xly_link"),
                "repo_name": validated_data.get("repo_name"),
                "model_name": validated_data.get("model_name"),
                "step_name": validated_data.get("step_name"),
                "tag_name": validated_data.get("tag_name"),
                "status": validated_data.get("status")
            })
