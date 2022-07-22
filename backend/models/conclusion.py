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


class CeConclusion(BaseModel, BaseModelMixin):
    """
    定义ce 的task表
    """
    __tablename__ = 'ce_release_conclusion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    branch = Column(VARCHAR(50), comment="提交分支")
    tag = Column(VARCHAR(50), comment="tag名或计划名")
    task_type = Column(VARCHAR(20), comment="任务的类型") #目前支持；model、frame、lite、infer、dist；表示一级别分类以及框架的按类处理
    conclusion = Column(Text, comment="测试结论")
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
