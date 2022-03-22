# !/usr/bin/env python3
# encoding: utf-8
"""
对外提供API逻辑，实现增删改查
"""
import asyncio
import json

from ce_web.settings.common import STORAGE
from exception import HTTP400Error
from libs.mongo.db import Mongo
from models.task_builds import CeTaskBuilds
from models.tasks import CeTasks

from api.forms import AddCaseForm
from views.base_view import MABaseView


class CaseDetailView(MABaseView):
    """
    完成模型kpi的快速存储
    """
    # 定义post类型检查类
    post_form_class = AddCaseForm

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        build_type_id: (获取任务的唯一id)
        build_id: 编译id
        repo: repo名
        branch: branch分支信息
        commit_id: commit 信息
        commit_time: commit 的提交信息
        build_time: 编包的时间
        job_id: 多阶段的job build id
        left_time: status=running中的剩余时间
        status: 任务状态
        exit_code: 任务本次执行的退出
        duration: 任务执行时长
        case_detail: case的执行详情
        """

        build_type_id = kwargs.get("build_type_id")
        build_id = kwargs.get("build_id")
        # task 入库逻辑
        task_obj = await CeTasks.aio_get_object(
            **{"build_type_id": build_type_id}
        )
        if not task_obj:
            # 不存在任务则抛出异常
            raise HTTP400Error("找不到任务，请先录入任务！")
        else:
            tid = task_obj.id
            # build 入库逻辑
            await CeTaskBuilds.create_or_update_build(
                tid, build_id, validated_data=kwargs
            )
            # case detail入库追加
            mongo_cfg = STORAGE["mongo"]['paddle_quality']
            table_name = mongo_cfg["case_detail"].format(
                task_id=tid, build_id=build_id
            )
            model_result = Mongo("paddle_quality", table_name)
            try:
                details = json.loads(kwargs.get("case_detail"))
            except:
                details = []

            for item in details:
                await model_result.insert(item)
            # 主动关闭mongodb的链接
            model_result.close()
