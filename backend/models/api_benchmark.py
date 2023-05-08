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

    uid = Column(Integer, comment='uid')
    routine = Column(Integer, comment='routine, 0: False, 1: True')
    comment = Column(VARCHAR(512), comment='comment')
    enable_backward = Column(Integer, comment='routine, 0: False, 1: True')
    python = Column(VARCHAR(255), comment='python')
    yaml_info = Column(VARCHAR(64), comment='yaml_info')
    wheel_link = Column(VARCHAR(1024), comment='paddle wheel link')

    description = Column(VARCHAR(256), comment='description')

    ci = Column(Integer, comment='ci任务标识, 0: False, 1: True')
    md5_id = Column(VARCHAR(100), comment='机器唯一标识码')
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


class ApiBenchmarkMission(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'apibm_mission'
    metadata = MetaData()
    id = Column(Integer, primary_key=True, autoincrement=True)
    # jid = Column(Integer)
    status = Column(VARCHAR(256), comment='运行状态，running， error， done')
    comment = Column(VARCHAR(256), comment='任务名/备注，随便写')
    with_gpu = Column(VARCHAR(256), comment='是否使用gpu，True/False')
    enable_backward = Column(VARCHAR(256), comment='是否开启反向，True/False')
    framework = Column(VARCHAR(256), comment='框架选择，paddle/torch')
    wheel_link = Column(VARCHAR(512), comment='框架版本信息，paddle支持链接或版本号，torch支持版本号')
    cuda = Column(VARCHAR(256), comment='cuda版本')
    python = Column(VARCHAR(256), comment='python版本')

    yaml_type = Column(VARCHAR(256), comment='是否使用默认配置，True/False')
    yaml_info = Column(VARCHAR(256), comment='yaml配置信息')

    # result = Column(VARCHAR(256), comment='结果')
    description = Column(VARCHAR(256), comment='xly请求描述')
    bos_url = Column(VARCHAR(256), comment='bos存储地址')
    # allure_report = Column(VARCHAR(256), comment='allure地址')
    create_time = Column(DateTime, comment="本记录创建的时间")
    update_time = Column(DateTime, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'api_benchmark'
