# !/usr/bin/env python3
# encoding: utf-8
"""
定义ce 的taks表
"""
from libs.mysql.db import BaseModel, BaseModelMixin, db_engines
from sqlalchemy import VARCHAR, BigInteger, Boolean, Column, Float, Integer, Text, DateTime, MetaData


class Job(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(VARCHAR(256), comment='描述，爱写啥写啥')
    status = Column(VARCHAR(256), comment='运行状态， running， error， done')
    version = Column(VARCHAR(200), comment='版本号的值， version， commit or pr array')
    compile =  Column(Integer, comment="编译任务外键")
    mission = Column(VARCHAR(512), comment='子任务外键集合 ， json string')
    create_time = Column(DateTime, comment="本记录创建的时间")
    update_time = Column(DateTime, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'framework'



class Compile(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'compile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    jid = Column(Integer)
    uid = Column(Integer)
    status = Column(VARCHAR(256), comment='运行状态， running， error， done')
    env = Column(VARCHAR(512), comment='环境配置信息')
    wheel = Column(VARCHAR(256), comment='编译包地址')
    os = Column(VARCHAR(512), comment='系统信息')
    pd_type = Column(VARCHAR(512), comment='commit，pr，tag')
    value = Column(VARCHAR(512), comment='值，可以是commit or pr or tag')
    branch = Column(VARCHAR(512), comment='分支信息')
    python = Column(VARCHAR(512), comment='python版本信息')
    cuda = Column(VARCHAR(512), comment='cuda信息')
    create_time = Column(DateTime, comment="本记录创建的时间")
    update_time = Column(DateTime, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'framework'


class Mission(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'mission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    jid = Column(Integer)
    status = Column(VARCHAR(256), comment='运行状态， running， error， done')
    module = Column(VARCHAR(256), comment='模块名字')
    result = Column(VARCHAR(256), comment='结果')
    description = Column(VARCHAR(256), comment='xly请求描述')
    bos_url = Column(VARCHAR(256), comment='bos存储地址')
    allure_report = Column(VARCHAR(256), comment='allure地址')
    create_time = Column(DateTime, comment="本记录创建的时间")
    update_time = Column(DateTime, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'framework'


class Settings(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'settings'
    option = Column(VARCHAR(256), primary_key=True)
    value = Column(VARCHAR(256))

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'framework'