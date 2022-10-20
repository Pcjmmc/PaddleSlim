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


class User(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'users_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50), comment='用户名')
    email = Column(VARCHAR(50), comment='邮件地址')
    identity = Column(VARCHAR(50), comment='身份标记是QA还是RD')
    departmentName = Column(VARCHAR(50), comment='部门信息')
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
