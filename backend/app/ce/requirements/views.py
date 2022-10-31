# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import (
    RPC_SETTINGS, TC_BASE_URL, XLY_BASE_URL, XLY_BASE_URL2
)
from ce_web.settings.scenes import back_dict, inner_dict, scenes_dict, selects
from libs.mongo.db import Mongo
from models.conclusion import CeConclusion
from models.icafe import CeIcafe
from models.release_version import CeReleaseVersion
from models.tasks import CeTasks
from rpc.icafe import CreateBug, GetBug

from views.base_view import MABaseView

PADDLE_ICAFE_USER = RPC_SETTINGS['paddle_icafe']['username']
PADDLE_ICAFE_PASSD = RPC_SETTINGS['paddle_icafe']['password']
baseUrl = "https://console.cloud.baidu-int.com/devops/icafe/issue/{space}-{sequence}/show"


class MangeIcafe(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        # 获取所有的处于新建、开发中、开发完成的卡片
        # 按照最后修改时间进行时间窗口筛选
        # TODO 讨论分页逻辑，现在初步看每个rd不会超过100张卡片，不设置
        # TODO 暂时不设置maxRecords和page
        begin_time = kwargs.get("begin_time")
        end_time = kwargs.get('end_time')
        if not begin_time or end_time:
            return None 
        rd = kwargs.get('rd')
        qa = kwargs.get('qa')
        iql = "流程状态 in (新建,开发中,开发完成) AND 类型 \
           in (Task,Bug,Story,任务) AND 最后修改时间 > {} AND 最后修改时间 < {}".format(begin_time, end_time)
        return await get_cards_by_filter(query)

    async def post(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
           # 新建卡片
        print("新建卡片")
        fields = kwargs.get("fileds")
        repo = fields.get("repo")
        bug_type = fields.get("bug_type")
        icafe_info = {
            "title": fields.get("title"),
            "type": "Bug",
            "detail": fields.get("description"),
            "fields": {},
            "creator": "liuhuanling"
        }
        content = ""
        if file_list:
            for item in file_list:
                img_content = item["content"]
                content +=  "<img src=\"{body}>".format(body=img_content)
                icafe_info["detail"] += "\n" + content

        icafe_info["fields"] = {
        }
        data = {
            "username": PADDLE_ICAFE_USER,
            "password": PADDLE_ICAFE_PASSD,
            "issues": [icafe_info]
        }
        result = await CreateBug(data).get_data()
        #  将icafe存起来；做关联关系
        issues = result.get("issues", [])
        print('创建参数', issues)
        if issues:
            sequence = issues[0].get("sequence")
            issues_url = issues[0].get("url")
            await CeIcafe.aio_insert(
                {'tid': tid,
                 'build_id': build_id,
                 'tag': plan_tag,
                 'issues_url':issues_url,
                 'sequence': sequence,
                 'secondary_type': secondary_type
                }
            )

async def get_cards_by_filter(query):
    """
    返回指定类型的数据详情
    """
    result = await GetBug({
        'u': PADDLE_ICAFE_USER,
        'pw': PADDLE_ICAFE_PASSD,
        'iql': query
    }).get_data()
    icafeData = result.get('cards', [])
    # 按照前端展示过滤下要展示的字段1
    result = []
    for item in icafeData:
        space = item.get('spacePrefixCode')
        sequence = item.get('sequence')
        level = ""
        rd_owner = ""
        qa_owner = ""
        properties = item.get("properties", [])
        for arr in properties:
            if arr.get("propertyName") == "优先级":
                level = arr.get("displayValue")
            elif arr.get("propertyName") == "QA负责人":
                qa_owner = arr.get("displayValue")
            elif arr.get("propertyName") == "RD负责人":
                rd_owner = arr.get("displayValue")
            elif arr.get("propertyName") == "bug发现方式":
                task_type = arr.get("value")
                displayValue = arr.get("displayValue")
        tmp = {
            "title": item.get("title"),
            "createdTime": item.get("createdTime"),
            "status": item.get("status"),
            "url": baseUrl.format(space=space, sequence=sequence),
            "level": level,
            "rd_owner": rd_owner,
            "qa_owner": qa_owner,
            "task_type": inner_dict.get(task_type) or displayValue,
            "log_url": await get_result_by_sequence(sequence)
        }
        result.append(tmp)
    return len(result), result


