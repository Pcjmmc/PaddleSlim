#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python


# 风险日报数据库配置更新
import asyncio
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)
print("PROJECT_DIR is", PROJECT_DIR)
from framework.config.release_daily_settings import RELEASE_DAILY_SETTINGS
from models.framework import ReleaseDailySettings


async def update_release_daily_settings():
    """
    更新脚本
    """
    for data in RELEASE_DAILY_SETTINGS:
        # 查询数据，有就更新，没有就插入
        res = await ReleaseDailySettings.aio_filter_count(module=data["module"])
        if res == 0:
            await ReleaseDailySettings.aio_insert(data)
        else:
            await ReleaseDailySettings.aio_update(data, params_data={"module": data["module"]})


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_release_daily_settings())