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


class Project(BaseModel, BaseModelMixin):
    """
    定义ce 的task表
    """
    __tablename__ = 'project_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    icafe_id = Column(Integer, comment="icafe卡片序列id")
    rd = Column(VARCHAR(60), comment="rd邮箱前缀")
    qa = Column(VARCHAR(60), comment="qa邮箱前缀")
    repo = Column(VARCHAR(60), comment="github repo")
    branch = Column(VARCHAR(30), comment="github repo branch")
    pr = Column(VARCHAR(60), comment="github repo pr info") 
    test_id = Column(Integer, comment="创建的测试服务对应的测试id")
    # 待测试、测试中、 通过、未通过 非别对应0，1，2，3
    test_status = Column(Integer, comment="测试服务对应的测试状态")
    #TODO 明确是否需要保留测试任务链接，是否可以通过test_id拼接出来
    test_url = Column(VARCHAR(100), comment="任务的类型") 
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
