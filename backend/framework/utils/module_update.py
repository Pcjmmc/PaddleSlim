#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

"""
用于更新数据库 前端 module 配置信息
"""
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)
print("PROJECT_DIR is", PROJECT_DIR)
from ce_web.settings.common import STORAGE

import asyncio
import json

from models.framework import Job, Mission, Compile, ModuleSettings
from datetime import datetime
from framework.config.module import module_mapping, module_list



async def update_module():
    """
    用于更新数据库 前端 module 配置信息
    """
    # 备份原有数据
    module_list_bak = await ModuleSettings.aio_filter_details(option="module_list")
    module_list_bak[0]["option"] = "module_list-" + str(datetime.now())
    res = await ModuleSettings.aio_insert(module_list_bak)
    if res[0] == 0:
        print("备份module_list 失败")
        exit(8)
    module_mapping_bak = await ModuleSettings.aio_filter_details(option="module_mapping")
    module_mapping_bak[0]["option"] = "module_mapping-" + str(datetime.now())
    res = await ModuleSettings.aio_insert(module_mapping_bak)
    if res[0] == 0:
        print("备份module_mapping 失败")
        exit(8)

    # 更新新数据
    await ModuleSettings.aio_update(validated_data={"value": json.dumps(module_list)}, params_data={"option": "module_list"})
    await ModuleSettings.aio_update({"value": json.dumps(module_mapping)}, {"option": "module_mapping"})


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_module())
