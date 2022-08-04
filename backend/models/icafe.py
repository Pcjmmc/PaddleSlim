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


class CeIcafe(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'ce_release_icafe_association'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tid = Column(Integer, comment="关联任务表中的任务id")
    tag = Column(VARCHAR(50), comment="tag名或计划名")
    secondary_type = Column(VARCHAR(100), comment="bug对应的二级分类")
    issues_url = Column(VARCHAR(200), comment="icafe地址")
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
