# !/usr/bin/env python3
# encoding: utf-8
"""
对外提供API逻辑，实现增删改查
"""
import asyncio
import copy
import json

from exception import HTTP400Error
from libs.mongo.db import Mongo
from models.details import CeCases
from models.publish_task_builds import PubishTaskBuilds
from models.tasks import CeTasks

from api.publish_forms import AddCaseForm
from views.base_view import MABaseView


class PublishCacheView(MABaseView):
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
        build_time: 任务执行时间（建议开始时间为准）
        job_id: 多阶段的job build id ,任务并行追加逻辑
        test_step: 任务现在的阶段；int型，从0开始以此对应阶段
        status: 任务状态
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
            params = copy.deepcopy(kwargs)
            params.pop("build_type_id")
            params.pop("build_id")
            await PubishTaskBuilds.create_or_update_build(
                tid, build_id, **params
            )

class UploadResultManage(MABaseView):
    """
    完成上传发布结果的result
    """
    async def post(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        接收到的数据原封不动的放到mongodb中
        """
        data_type = kwargs.get('data_type')
        version = kwargs.get('version')
        appid = kwargs.get('appid', 1)
        data = kwargs.get('data')
        if data and version:
            if data_type == 'bos':
                table_name = 'publish_bos_{version}_{appid}'.format(
                    version=version, appid=appid
                )
            else:
                table_name = 'publish_other_{version}_{appid}'.format(
                    version=version, appid=appid
                )
            table_result = Mongo("paddle_quality", table_name)
            # 整个过程都是直接删除，重新创建表
            await table_result.delete_coll()
            await table_result.insert(json.loads(data))
        else:
            raise HTTP400Error("请检查，data或version是否为空")
