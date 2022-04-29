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
from models.details import CeCases

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
        build_type_id: (获取任务的唯一id)，效率云对应AGILE_PIPELINE_CONF_ID
        build_id: 构建id，效率云对应AGILE_PIPELINE_BUILD_ID
        repo: repo名#被测对象，框架Paddle，模型对应repo
        branch: branch分支信息
        commit_id: commit 信息
        commit_time: commit 的提交信息
        build_time: 编包的时间
        job_id: 多阶段的job build id ,任务并行追加逻辑
        left_time: status=running中的剩余时间
        status: 任务状态
        exit_code: 任务本次执行的退出
        duration: 任务执行时长
        case_detail: case的执行详情
        """

        build_type_id = kwargs.get("build_type_id")
        build_id = kwargs.get("build_id")
        status = kwargs.get("status")
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
            #TOTO插入case之前需要先判断之前是否存在对应表名
            model_result = Mongo("paddle_quality", table_name)
            try:
                details = json.loads(kwargs.get("case_detail"))
            except:
                details = []
            total = len(details)
            passed_num = 0
            for item in details:
                if "kpi_status" in item.keys() and item["kpi_status"] == "Passed":
                    passed_num += 1
                await model_result.insert(item)
            failed_num = total - passed_num
            # 主动关闭mongodb的链接
            model_result.close()
            # case详细入库mysql 
            await CeCases.create_or_update_build(build_type_id, build_id, status, total, passed_num, failed_num)
