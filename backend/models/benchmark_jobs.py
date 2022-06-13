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
from sqlalchemy import VARCHAR, BigInteger, Boolean, Column, Float, Integer, Text, DateTime


class BenchmarkJobs(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(VARCHAR(255), comment='任务结果')
    mode = Column(VARCHAR(255), comment='状态')
    paddle_commit = Column(VARCHAR(64), comment='paddle commit信息')
    paddle_version = Column(VARCHAR(64), comment="paddle的版本")
    torch_version = Column(VARCHAR(64), comment="torch的版本")
    create_time = Column(DateTime, comment="创建时间")
    update_time = Column(DateTime, comment="更新时间")
    hostname = Column(VARCHAR(255), comment="服务名")
    place = Column(VARCHAR(255), comment="设备")
    card = Column(VARCHAR(255), comment="显卡")
    system = Column(VARCHAR(255), comment="系统")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'api_benchmark'
