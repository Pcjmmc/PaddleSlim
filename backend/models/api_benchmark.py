#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
定义benchmark 表
"""
from libs.mysql.db import BaseModel, BaseModelMixin, db_engines
from sqlalchemy import VARCHAR, BigInteger, Boolean, Column, Float, Integer, Text, DateTime, MetaData


class Job(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'job'
    metadata = MetaData()
    id = Column(Integer, primary_key=True, autoincrement=True)
    framework = Column(VARCHAR(256), comment='paddle torch')
    status = Column(VARCHAR(256), comment='运行状态， running， error， done')
    mode = Column(VARCHAR(256), comment='rerun etc.')
    commit = Column(VARCHAR(256), comment='commit')
    version = Column(VARCHAR(200), comment='版本号的值， version')
    hostname = Column(VARCHAR(256), comment='hostname')
    place = Column(VARCHAR(256), comment='place')
    system = Column(VARCHAR(256), comment='system')
    cuda = Column(VARCHAR(32), comment='cuda')
    cudnn = Column(VARCHAR(32), comment='cudnn')
    snapshot = Column(VARCHAR(1024), comment='snapshot')
    create_time = Column(DateTime, comment="本记录创建的时间")
    update_time = Column(DateTime, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'api_benchmark'



class Case(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'case'
    metadata = MetaData()
    id = Column(Integer, primary_key=True, autoincrement=True)
    jid = Column(Integer)
    case_name = Column(VARCHAR(256), comment='运行状态， running， error， done')
    api = Column(VARCHAR(256), comment='运行状态， running， error， done')
    result = Column(VARCHAR(256), comment='运行状态， running， error， done')
    create_time = Column(DateTime, comment="本记录创建的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'api_benchmark'


class Settings(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'settings'
    metadata = MetaData()
    option = Column(VARCHAR(256), primary_key=True)
    value = Column(VARCHAR(256))

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'api_benchmark'