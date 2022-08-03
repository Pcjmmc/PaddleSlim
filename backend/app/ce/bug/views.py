# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import RPC_SETTINGS
from ce_web.settings.scenes import back_dict, inner_dict, scenes_dict, selects
from libs.mongo.db import Mongo
from models.conclusion import CeConclusion
from models.icafe import CeIcafe
from rpc.icafe import CreateBug, GetBug

from views.base_view import MABaseView

PADDLE_ICAFE_USER = RPC_SETTINGS['paddle_icafe']['username']
PADDLE_ICAFE_PASSD = RPC_SETTINGS['paddle_icafe']['password']
baseUrl = "https://console.cloud.baidu-int.com/devops/icafe/issue/{space}-{sequence}/show"


class BugManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        # 获取所有的bug卡片, 根据plan tag 和 类型来查询
        ptag = kwargs.get("tag")
        task_type = kwargs.get("task_type")
        if task_type:
            # 根据方向查询
            # 将task_type 转化成查询条件
            task_type = back_dict.get(task_type)
            query = 'plan_tag ~ {ptag} AND 类型 = Bug AND bug发现方式 = {task_type} AND repo = Paddle'.format(
            ptag=ptag, task_type=task_type)
            return await self.get_bugs_by_filter(query)
        else:
            # 查询全量
            condition = ",".join(selects)
            query = 'repo = Paddle AND bug发现方式 in ({condition}) AND plan_tag ~ {ptag} AND 类型 = Bug'.format(
                condition=condition, ptag=ptag
            )
            return await self.get_all_bugs(query)

    async def get_bugs_by_filter(self, query):
        """
        返回指定类型的数据详情
        """
        result = await GetBug({
            'u': PADDLE_ICAFE_USER,
            'pw': PADDLE_ICAFE_PASSD,
            'iql': query
        }).get_data()
        bugData = result.get('cards', [])
        # 过滤下数据，太多了
        result = []
        for item in bugData:
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
            tmp = {
                "title": item.get("title"),
                "createdTime": item.get("createdTime"),
                "status": item.get("status"),
                "url": baseUrl.format(space=space, sequence=sequence),
                "level": level,
                "rd_owner": rd_owner,
                "qa_owner": qa_owner
            }
            result.append(tmp)
        return len(result), result

    async def get_all_bugs(self, query):
        """
        返回统计数据；按状态统计；按bug的发现方式统计
        """
        result = await GetBug({
            'u': PADDLE_ICAFE_USER,
            'pw': PADDLE_ICAFE_PASSD,
            'iql': query
        }).get_data()
        bugData = result.get('cards', [])
        # 过滤下数据，太多了
        process = {}
        distribution = {}
        for item in bugData:
            task_type = None
            status = item.get("status")
            if status not in process:
                process[status] = 0
            process[status] += 1
            properties = item.get("properties", [])
            for i in properties:
                if i.get("propertyName") == "bug发现方式":
                    task_type = i.get("value")
                    task_type = inner_dict.get(task_type)
                    break
            if task_type and task_type not in distribution:
                distribution[task_type] = 0
            if task_type:
                distribution[task_type] += 1
        results = {
            "sts_datas": [{"value": val, "name": key} for key, val in process.items()],
            "sts_column": list(process.keys()),
            "dis_datas": list(distribution.keys()),
            "dis_count": list(distribution.values())
        }
        return len(results), results

    async def post(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        try:
            fields = json.loads(kwargs.get("data"))
        except:
            fields = {}
        try:
            file_list = json.loads(kwargs.get("images"))
        except:
            file_list = []
        issues_url = fields.get("issues_url")
        plan_tag = fields.get("tag")
        tid = fields.get('tid')
        if issues_url:
            # 走关联卡片
            print("关联已有卡片")
            await CeIcafe.aio_insert({'tid': tid, 'tag':plan_tag, 'issues_url':issues_url})
        else:
            # 新建卡片
            print("新建卡片")
            repo = fields.get("repo")
            bug_type = fields.get("bug_type")
            icafe_info = {
                "title": fields.get("title"),
                "type": "Bug",
                "detail": fields.get("description"),
                "所属计划": "飞桨项目集/Paddle/{tag}".format(tag=plan_tag),
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
                "负责人": fields.get("rd_owner"),
                "需求来源": "QA团队",
                "负责人所属团队": "基础框架-训练",
                "QA负责人" : fields.get("qa_owner"),
                "RD负责人" : fields.get("rd_owner"),
                "流程状态" : "新建",
                "plan_tag" : plan_tag,
                "repo": repo,
                "bug发现方式": bug_type,
                "优先级": fields.get("level")
            }
            data = {
                "username": PADDLE_ICAFE_USER,
                "password": PADDLE_ICAFE_PASSD,
                "issues": [icafe_info]
            }
            result = await CreateBug(data).get_data()
            #  将icafe存起来；做关联关系
            issues = result.get("issues", [])
            if issues:
                issues_url = issues[0].get("url")
                await CeIcafe.aio_insert({'tid': tid, 'tag':plan_tag, 'issues_url':issues_url})


class ConclusionManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        result = {}
        query_param = {}
        tag = kwargs.get("tag")
        branch = kwargs.get("branch")
        if tag:
            query_param["tag"] = tag
        if branch:
            query_param["branch"] = branch
        records = await CeConclusion.aio_filter_objects(**query_param)
        # 将数据组装成1条
        result = {res.task_type: res.conclusion for res in records if res.task_type != "model"}

        # 将models组装好
        models = {res.model_repo: res.conclusion for res in records if res.task_type == "model"}

        result["model"] = models

        return len(result), result

    async def post(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        try:
            data = json.loads(kwargs.get('data', ''))
        except:
            data = []
        for item in data:
            query_param = {
                "branch": item.get("branch"),
                "tag": item.get("tag"),
                "task_type": item.get("task_type"),
                "model_repo": item.get("model_repo")
            }
            await CeConclusion.aio_delete(params_data=query_param)
        await CeConclusion.aio_insert(validated_data=data)
