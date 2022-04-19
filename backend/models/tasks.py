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


class CeTasks(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'ce_task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tname = Column(VARCHAR(200), comment='任务名') # xly: ''; tc: %system.teamcity.buildConfName%
    # workspace = Column(VARCHAR(200), comment='所属的空间名') # xly：AGILE_WORKSPACE； tc:非必需，填写上一级的名字%system.teamcity.projectName% 
    owner = Column(VARCHAR(50), comment="任务所属人")
    build_type_id = Column(VARCHAR(255), comment="任务的build type") # xly： "pipelineConfId;得确定下这个值唯一吗"； teamcity："%system.teamcity.buildType.id%"
    platform = Column(VARCHAR(50), comment="任务所属平台") # tc or xly?
    system = Column(VARCHAR(50), comment="任务所属平台") # 测试的系统信息：Linux_gpu、T4、Xpu、 jetson、windows、mac等?
    description = Column(VARCHAR(100), comment="任务的概述") # 要求概述简单明了
    task_type = Column(VARCHAR(20), comment="任务的类型") #目前支持；model、frame、lite、infer、dist；表示一级别分类以及框架的按类处理
    secondary_type = Column(VARCHAR(50), comment="任务的二级类型") #二级分类
    dependencies = Column(VARCHAR(100), comment="依赖的上游编译任务") # xly： "pipelineConfId;得确定下这个值唯一吗"； teamcity："%system.teamcity.buildType.id%"
    step = Column(VARCHAR(20), comment="任务所属的阶段") # compile: 编译任务； 下游任务有分成： develop； release；shared;
    appid = Column(Integer, comment="任务所属的app")
    reponame = Column(VARCHAR(50), comment="任务所属的repo")
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'paddle_quality'
