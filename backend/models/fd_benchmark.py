#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  fd_benchmark.py
  * @author:  luozeyu01
  * @date  2023/3/30 3:44 PM
  * @brief 
  *
  **************************************************************************/
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
    uid = Column(Integer)
    routine = Column(Integer, comment='routine, 0: False, 1: True')
    comment = Column(VARCHAR(256), comment='描述，爱写啥写啥')
    status = Column(VARCHAR(256), comment='运行状态， running， error， done')
    fork = Column(VARCHAR(256), comment='github克隆代码库')
    branch = Column(VARCHAR(256), comment='github代码库分支')
    mission = Column(VARCHAR(512), comment='多硬件子任务外键集合 ， json string')
    # bos_path = Column(VARCHAR(256), comment='bos储存地址')
    create_time = Column(DateTime, comment="本记录创建的时间")
    update_time = Column(DateTime, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'fd_benchmark'


class Mission(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'mission'
    metadata = MetaData()
    id = Column(Integer, primary_key=True, autoincrement=True)
    jid = Column(Integer)
    uid = Column(Integer)
    routine = Column(Integer, comment='routine, 0: False, 1: True')
    status = Column(VARCHAR(256), comment='运行状态， running， error， done')
    module = Column(VARCHAR(256), comment='硬件种类')
    compile = Column(VARCHAR(1024), comment='编译参数，json string')
    commit = Column(VARCHAR(1024), comment='包的commit版本，json string')
    # repo_commit = Column(VARCHAR(1024), comment='库的commit版本，json string')
    version = Column(VARCHAR(32), comment='包的版本号')
    # result = Column(VARCHAR(256), comment='多硬件mission运行结果')
    description = Column(VARCHAR(256), comment='xly请求描述')
    info = Column(VARCHAR(256), comment='info 任务链接信息')
    bos_path = Column(VARCHAR(256), comment='bos存储地址')
    snapshot = Column(VARCHAR(1024), comment='snapshot')
    create_time = Column(DateTime, comment="本记录创建的时间")
    update_time = Column(DateTime, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'fd_benchmark'


class Case(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'case'
    metadata = MetaData()
    id = Column(Integer, primary_key=True, autoincrement=True)
    jid = Column(Integer)
    model = Column(VARCHAR(256), comment='模型名')
    backend = Column(VARCHAR(256), comment='使用后端, 例如 gpu_paddle_trt_fp32')
    result = Column(VARCHAR(256), comment='结果数据, 例如 {"End2End(ms)": 569.344, "cpu_rss_mb": 412.355')
    create_time = Column(DateTime, comment="本记录创建的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'fd_benchmark'
