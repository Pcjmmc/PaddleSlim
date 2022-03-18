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


class CeExempt(BaseModel, BaseModelMixin):
    """
    定义ce 的task表
    """
    __tablename__ = 'ce_exempt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(Integer, comment='归属的发版id')
    tid = Column(Integer, comment="关联任务表中的任务id")
    status = Column(Boolean, comment='阶段当前的状态') # true: 表示豁免； false:表示没有豁免
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
