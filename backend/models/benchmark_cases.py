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


class BenchmarkCases(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    jid = Column(Integer)
    case_name = Column(VARCHAR(255), comment='case名字')
    result = Column(VARCHAR(1024), comment='case详情')
    create_time = Column(DateTime, comment="创建时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'api_benchmark'
