"""
负责menu的操作逻辑，为其他view提供封装的逻辑
"""
# encoding=utf-8
import json
import asyncio
import copy
import os
import sys

import aiohttp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo
from models.release_version import CeReleaseVersion


async def update_menu(appid=1):
    # CeReleaseVersion 表重新组装menu的release
    # 这里的逻辑全部都是基础框架的，所以appid默认为1即可，
    # 其他的等开发的时候能公用就公用，不能就重写
    table_name = "ce_menu_{appid}".format(appid=appid)
    menu_db = Mongo("paddle_quality", table_name)
    result = await menu_db.find_all()
    menuDesc = result[0] if result else {}
    menuDescContent = json.loads(menuDesc['content'])
    menu_info = await CeReleaseVersion().aio_filter_details(need_all=True, order_by="-created")
    if menu_info:
        # 如果有则需要需要将原来的menu内容重置掉，重新写入最新信息
        menuDescContent.pop("version")
        # 初始化成空的状态
        menuDescContent["version"] = []
    for item in menu_info:
        name = item.get("name")
        menuDescContent["version"].append({"name": name, "desc": name})
    menuDesc['content'] = json.dumps(menuDescContent)
    await menu_db.update(menuDesc)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_menu())

