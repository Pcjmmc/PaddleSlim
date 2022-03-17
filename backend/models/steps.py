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


class CeSteps(BaseModel, BaseModelMixin):
    """
    定义ce 的task表
    """
    __tablename__ = 'ce_steps'
    id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(Integer, comment='归属的发版id')
    rtype = Column(VARCHAR(50), comment='阶段类型')
    content = Column(VARCHAR(50), comment='阶段描述')
    status = Column(VARCHAR(20), comment='阶段当前的状态')
    flag = Column(VARCHAR(20), comment='当前阶段是否选中')
    order = Column(Integer, comment="阶段的顺序")
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'ce'
