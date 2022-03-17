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


class CeReleaseVersion(BaseModel, BaseModelMixin):
    """
    定义ce 的task表
    """
    __tablename__ = 'ce_release_version'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), comment='版本名')
    branch = Column(VARCHAR(50), comment="提交分支")
    tag = Column(VARCHAR(50), comment="tag名或计划名")
    pre_tag = Column(VARCHAR(50), comment="上一次的tag名")
    begin_time = Column(Integer, comment="commit的开始时间")
    end_time = Column(Integer, comment="commit的结束时间")
    begin_commit = Column(VARCHAR(100), comment= '即上一次打tag时的commit id,与begin_time照应')
    end_commit = Column(VARCHAR(100), comment= '本次打tag时的commit，与end_time照应')
    activated = Column(Boolean, comment="是否激活, False:已归档")
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'ce'
