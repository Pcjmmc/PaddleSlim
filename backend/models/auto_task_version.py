"""
动态创建表并且动态映射表，适用于分表
"""
# encoding: utf-8
import asyncio
import os
import sys
import traceback

import sqlalchemy as sa
from sqlalchemy import VARCHAR, Column, Float, Integer, MetaData, Table, Boolean

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from libs.mysql.db import BaseModelMixin

class TaskVersion(BaseModelMixin):
    """
    约定动态表之后映射的类
    """
    class Meta:
        """
        定义定义相应的类，以及model所属的库
        app_label与动态表结构的db_key一致
        """
        app_label = 'paddle_quality'


class TaskTableObj(object):
    """
    约定动态建表，分表的表结构
    """
    def __init__(self, db_key, table_name):
        self.db_key = db_key
        self.table_name = table_name
    
    def get_table_obj(self):
        metadata = MetaData()
        table_object = Table(self.table_name, metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('tname', VARCHAR(200), comment='任务名'),
            Column('show_name', VARCHAR(200), comment='任务名'),
            Column('workspace', VARCHAR(50), comment='所属的空间名'),
            Column('owner', VARCHAR(50), comment="任务所属人"),
            Column('build_type_id', VARCHAR(255), comment="任务的build type"),
            Column('platform', VARCHAR(50), comment="任务所属平台"),
            Column('system', VARCHAR(50), comment="任务所属平台"),
            Column('description', VARCHAR(100), comment="任务的概述"),
            Column('task_type', VARCHAR(20), comment="任务的类型"),
            Column('secondary_type', VARCHAR(100), comment="任务的二级类型"),
            Column('release_source', VARCHAR(50), comment="tag之后编译任务发布源"),
            Column('dependencies', VARCHAR(100), comment="依赖的上游编译任务"),
            Column('step', VARCHAR(20), comment="任务所属的阶段"),
            Column('is_offline', Boolean, comment="是否下线, True:已下线; False:为下线"),
            Column('appid', Integer, comment="任务所属的app"),
            Column('reponame', VARCHAR(50), comment="任务所属的repo"),
            Column('created', Integer, comment="本记录创建的时间"),
            Column('updated', Integer, comment="本记录更新的时间"),
        )
        return table_object

