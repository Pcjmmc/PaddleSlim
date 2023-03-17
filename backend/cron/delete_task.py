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

def get_system(origin_env):
    env = origin_env.strip()
    envs = env.split('-')
    if 'Cuda' in envs[1]:
        lens = len(envs[1])
        new_str = envs[1][0:lens-1] + '.'+envs[1][-1]
        envs[1] = new_str
        envs.insert(1,'Gpu')
    return '_'.join(envs)

def get_step(step):
    if step.lower() in ['develop', 'dev']:
        return 'develop'
    elif step.lower() in ['release']:
        return 'release'
    else:
        return step

async def save_task(file_path):
    """
    批量录入任务脚本，解析并录入任务
    """
    # 根据文件路径拼好数据上传
    file_name = open(file_path, 'r', encoding="utf-8")
    for line in file_name.readlines():
        line = line.strip()
        info = line.split()
        # record = {
        #   'tname': info[0],
        #   'show_name': info[1],
        #   'secondary_type': info[2],
        #   'reponame': info[3],
        #   'system': get_system(info[4]),
        #   'build_type_id': info[5],
        #   'workspace': info[6],
        #   'owner': info[7],
        #   'task_type': 'model',
        #   'step': get_step(info[8]),
        #   'description': info[8] +'下模型任务'+info[2]+'例行',
        #   'platform': 'xly'
        # }
        record = {
          'tname': info[0],
          'secondary_type': info[1],
          'reponame': info[2],
          'system': get_system(info[3]),
          'build_type_id': info[4],
          'workspace': info[5],
          'owner': info[6],
          'task_type': 'model',
          'step': get_step(info[7]),
          'description': info[7] +'下模型任务'+info[1]+'例行',
          'platform': 'xly'
        }
        print(record)
        await CeTasks().aio_insert(validated_data=record)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        save_task("/Users/liuhuanling/project/baidu/paddle/paddletest/backend/task.txt")
    )
