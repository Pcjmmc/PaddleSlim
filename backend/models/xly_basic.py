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


class XlyBasic(BaseModel, BaseModelMixin):
    """
    定义tasks任务的执行是的表结构
    """
    __tablename__ = 'xly_basic_info'
    conf_id = Column(Integer, primary_key=True, comment="任务配置id对应效率云AGILE_PIPELINE_CONF_ID") 
    workspace = Column(VARCHAR(60), comment="任务项目名称对应效率云AGILE_WORKSPACE")
    jobname = Column(VARCHAR(60), comment="任务项目名称对应效率云AGILE_PIPELINE_NAME")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
