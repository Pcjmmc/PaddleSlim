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
from sqlalchemy import VARCHAR, BigInteger, Boolean, Column, Float, Integer, Text


class PubishResult(BaseModel, BaseModelMixin):
    """
    定义tasks任务的执行是的表结构
    """
    __tablename__ = 'publish_result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(VARCHAR(50), comment="版本号")
    source = Column(VARCHAR(50), comment="发布源")
    content = Column(VARCHAR(255), comment="发布内容概述")
    url = Column(VARCHAR(200), comment="发布源地址")
    created = Column(Integer, comment="任务本次构建的开始时间，单位秒")
    updated = Column(Integer, comment="本条记录的修改时间，单位秒")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
