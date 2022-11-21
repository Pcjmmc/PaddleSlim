# encoding: utf-8
import asyncio
import copy
import json
import os
import sys

import aiohttp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from ce_web.settings.common import STORAGE
from libs.mysql.db import AutoCreateTableManager
from models.auto_task_version import TaskTableObj, TaskVersion

async def create_task_backup(db_key, table_name, need_create=False):
    """
    创建task 任务的备份表，用来存储当时发版时的任务信息
    """
    table_obj = TaskTableObj(db_key, table_name)
    creator = AutoCreateTableManager(TaskVersion, table_obj)
    # 若没有会创建新的表，若有则创建失败
    if need_create:
        # 只有打tag的时候需要动态创建一次，其他的都无需创建
        await creator.construct_table()
    return creator.map_class_to_table()
