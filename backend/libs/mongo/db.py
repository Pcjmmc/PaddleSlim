# !/usr/bin/env python3
# encoding: utf-8
"""
Define Mongo Manager
"""
import json
import asyncio
import os
import sys

import aiohttp
import motor.motor_asyncio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)
print("PROJECT_DIR is", PROJECT_DIR)
from ce_web.settings.common import STORAGE


class Mongo:
    """包装motor访问DB
    """

    def __init__(self, database, collection_name):
        """
        :param database: Mongo的DB名称
        :param collection_name: DB下面collection的名字
        """
        mongo_cfg = STORAGE["mongo"][database]
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            mongo_cfg["host"], mongo_cfg["port"],
            username=mongo_cfg["user"],
            password=mongo_cfg["password"],
            #authSource=mongo_cfg["db_name"]
        )
        self.db = self.client[mongo_cfg['db_name']]
        self.coll = self.db[collection_name]


    async def insert(self, data):
        """
        插入新记录
        :param data: 待插入的数据
        :return : 新增记录的 ObjectId
        """
        ret = await self.coll.insert_one(data)
        return ret.inserted_id if ret else None

    async def insert_many(self, data):
        """
        插入多行新记录
        :param data: 待插入的数据
        :return : 新增记录的 ObjectId
        """
        ret = await self.coll.insert_many(data)
        return ret.inserted_ids if ret else None


    async def update(self, data):
        """更新一条已有记录，实际使用的是mongo的replace
        """
        ret = await self.coll.find_one_and_replace(
            {"_id": data["_id"]}, data)
        return ret["_id"] if ret else None

    async def find_one(self, condition):
        """查找一条记录
        """
        return await self.coll.find_one(condition)

    async def find(self, condition):
        """根据条件查找
        """
        return await self.coll.find(condition).to_list(None)

    async def find_all(self):
        return await self.coll.find().to_list(None)

    async def delete(self, condition):
        """根据条件删除记录
        """
        return await self.coll.delete_many(condition)

    async def get_count_by_condition(self, condition):
        """根据条件查找
        """
        return await self.coll.count_documents(condition)

    async def get_data_and_count_by_condition(self, condition):
        """
        根据条件查询数量和数据
        """
        job_task = []
        job_task.append(self.get_count_by_condition(condition))
        job_task.append(self.find(condition))
        result = await asyncio.gather(*job_task)
        return result[0], result[1]
    
    async def delete_coll(self):
        print("begin delet table", self.coll)
        res = await self.db.drop_collection(self.coll)
        msg = res.get("errmsg")
        if not msg:
           return True
        return False

    def close(self):
        print("close mongodb...", flush=True)
        self.client.close()


if __name__ == "__main__":
    # 调用示例，初始化menu数据
    loop = asyncio.get_event_loop()
    appid=1
    table_name = 'ce_menu_{appid}'.format(appid=appid)
    menu_obj = Mongo('paddle_quality', table_name)
    menuDesc = {
        "version": [
        ],
        "requirement": {
            "desc": "需求",
            "icon": "ios-star-outline"
        },
        "test": {
            "desc": "测试",
            "icon": "ios-bulb-outline",
            "sub": {
                "history": {
                    "desc": '历史记录'
                },
                "package": {
                    "desc": '编包列表'
                },
            }
        },
        "integration": {
            "desc": "集测",
            "icon": "ios-analytics"
        },
        "publish": {
            "desc": "发布",
            "icon": "ios-cloud-upload-outline"
        },
        "config": {
            "desc": '测试能力管理',
            "icon": 'ios-paper',
            "sub": {
                "jobs": {
                    "desc": '任务注册',
                },
                "binary": {
                    "desc": '二分查找'
                }
            }
        },
        "framework": {
            "desc": '框架测试服务(PTS)',
            "sub": {
              "service": {"desc": '创建任务'},
              "detail": {"desc": '任务查询'}
            }
        },
        "detail": {
            "sub": {
                "function": {"desc": '功能详情'},
                "model": {"desc": '模型详情'},
                'test-detail': {"desc": '测试详情'},
                'frame-api-detail': {"desc": '基础框架详情'},
                'commit-detail': {"desc": 'commit 覆盖信息'}
            },
            "notMenu": True
        },
        "login": {
            "desc": '登录',
            "notMenu": True
        }
    }
    menuDesc = json.dumps(menuDesc)
    loop.run_until_complete(menu_obj.insert({"content": menuDesc}))

