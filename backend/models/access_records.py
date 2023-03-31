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
from sqlalchemy import VARCHAR, Column, Integer
from utils.md5 import get_md5


class AccessRecords(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'user_access_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    banckend_func = Column(VARCHAR(200), comment='后端函数名')
    method = Column(VARCHAR(20), comment='方法名')
    uid = Column(Integer, comment='用户id')
    fronted_url = Column(VARCHAR(255), comment='前端页面路径')
    response_time = Column(Integer, comment="请求的响应时间")
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
