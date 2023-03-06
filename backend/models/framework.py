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
    uid = Column(Integer)
    description = Column(VARCHAR(256), comment='描述，爱写啥写啥')
    status = Column(VARCHAR(256), comment='运行状态， running， error， done')
    version = Column(VARCHAR(200), comment='版本号的值， version， commit or pr array')
    compile =  Column(Integer, comment="编译任务外键")
    mission = Column(VARCHAR(512), comment='子任务外键集合 ， json string')
    is_deleted = Column(Integer, comment='删除状态')
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
    is_deleted = Column(Integer, comment='删除状态')
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
    is_deleted = Column(Integer, comment='删除状态')
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


class ModuleSettings(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'module_settings'
    option = Column(VARCHAR(256), primary_key=True)
    value = Column(Text(2048))

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'framework'


class FeedBack(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer)
    star = Column(Integer)
    content = Column(Text(2048), comment='反馈内容')
    username = Column(VARCHAR(256), comment='用户名')
    create_time = Column(DateTime, comment="本记录创建的时间")
    update_time = Column(DateTime, comment="本记录更新的时间")

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'framework'


class ReleaseDailySettings(BaseModel, BaseModelMixin):
    """
    定义ReleaseDailySettings任务的表结构
    """
    __tablename__ = 'release_daily_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    module = Column(VARCHAR(256), comment='模块名')
    order = Column(Integer)
    owner = Column(VARCHAR(256), comment='负责人')

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'framework'


class ReleaseDailyContent(BaseModel, BaseModelMixin):
    """
    定义RReleaseDailyContent任务的表结构
    """
    __tablename__ = 'release_daily_content'
    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, comment='模块名')
    content = Column(Text(2048))
    user = Column(VARCHAR(256), comment='提交人')
    version = Column(VARCHAR(256), comment='版本')
    create_time = Column(DateTime, comment='负责人')

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'framework'
