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


async def update_menu():
    # CeReleaseVersion 表重新组装menu的release
    table_name = "ce_menu"
    menu_db = Mongo("ce", table_name)
    result = await menu_db.find_all()
    menuDesc = result[0] if result else {}
    menuDescContent = json.loads(menuDesc['content'])
    menu_info = await CeReleaseVersion().aio_filter_details(need_all=True)
    if menu_info:
        # 如果有则需要需要将原来的menu内容重置掉，重新写入最新信息
        menuDescContent["release"].pop("sub")
        # 初始化成空的状态
        menuDescContent["release"]["sub"] = {
            "tag": {
                "desc": "历史记录",
                "icon": "ios-folder",
                "sub": {}
            }
        }
    for item in menu_info:
        activated = item.get("activated")
        name = item.get("name")
        if activated:
            key = name.split("release/")[-1] if "release/" in name else name
            menuDescContent["release"]["sub"][key] = {"desc": name}
        else:
            menuDescContent["release"]["sub"]["tag"]["sub"][name] = {"desc": name}
    copyMenu = copy.deepcopy(menuDescContent)
    if len(menuDescContent["release"]["sub"]) == 2:
        # 为了调整下menu的顺序; 将正在发版的放在历史数据的前面；即现将tag弹出，再插入
        copyMenu["release"]["sub"].pop("tag")
        copyMenu["release"]["sub"]["tag"] = menuDescContent["release"]["sub"]["tag"]
    menuDesc['content'] = json.dumps(copyMenu)
    await menu_db.update(menuDesc)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_menu())

