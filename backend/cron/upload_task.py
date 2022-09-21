"""
批量录入任务脚本
"""
# !/usr/bin/env python3
# encoding: utf-8
import asyncio
import os
import shutil
import sys

import aioredis
import wget
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from models.tasks import CeTasks

OWNER = "xieyunshen"
platform = "xly"
task_type= "compile"
step = "publish"
secondary_type="预测-Linux"
release_source="pypi/bos"
description = "Linux预测发版编译"

async def save_task(file_path):
    """
    批量录入任务脚本，解析并录入任务
    """
    # 根据文件路径拼好数据上传
    file_name = open(file_path, 'r', encoding="utf-8")
    for line in file_name.readlines():
        line = line.strip()
        info = line.split()
        tname = info[0]
        build_type_id = info[1]
        workspace = info[2]
        system = info[3]
        record = {
          'tname': tname,
          'owner': OWNER,
          'build_type_id': build_type_id,
          'platform': platform,
          'system': system,
          'task_type': task_type,
          'description': description,
          'step': step,
          'secondary_type': secondary_type,
          'workspace': workspace,
          'release_source': release_source
        }
        print(record)
        await CeTasks().aio_insert(validated_data=record)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        save_task("/Users/liuhuanling/project/baidu/paddle/paddletest/backend/task.txt")
    )
