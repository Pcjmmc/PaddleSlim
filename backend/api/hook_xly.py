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
from models.xly_basic import XlyBasic
from models.xly_build import XlyBuild
from models.details import CeCases

from api.xly_forms import XlyForm
from api.cache import BuildCacheBase
from views.base_view import MABaseView


class HookxlyView(MABaseView):
    """
    完成效率云的任务hook数据获取和存储
    """
    # 定义post类型检查类
    post_form_class = XlyForm
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        build_type_id: (获取任务的唯一id)，效率云对应AGILE_PIPELINE_CONF_ID
        build_id: 构建id，效率云对应AGILE_PIPELINE_BUILD_ID
        job_id: 多阶段的job build id ,任务并行追加逻辑
        status: 任务状态
        case_detail: case的执行详情
        """
        remote_ip = self.request.remote_ip
        header = self.request.headers
        status = header.get("BUILD_STATUS", "")
        print("status=", header.get("BUILD_STATUS", ""))
        print("conf_id=", kwargs.get('conf_id'), "build_id=", kwargs.get('build_id'), "job_id=", kwargs.get('job_id'))
        xly_basic = {}
        xly_build = {}
        if "RUNNING" == status:
            xly_basic['conf_id'] = kwargs.get("conf_id")
            xly_basic['workspace'] = kwargs.get("workspace")
            xly_basic['jobname'] = kwargs.get("jobname")
            print(xly_basic)
            await XlyBasic.aio_insert(xly_basic)
            xly_build['build_id'] = kwargs.get("build_id")
            xly_build['job_id'] = kwargs.get("job_id")
            xly_build['conf_id'] = kwargs.get("conf_id")
            xly_build['status'] = status
            xly_build['begin_ime'] = kwargs.get("begin_time")
            print(xly_build)
            await XlyBuild.aio_insert(xly_build)
        if status in ["FAIL", "SUCC", "CANCEL"]:
            job_id = kwargs.get("job_id")
            xly_build["exit_code"] = header.get("exit_code", None)
            xly_build["end_time"] = kwargs.get("end_time")
            print(xly_build)
            #考虑到任务如果被重复触发buildid不变，但是jobid变化，设置jobid为主键
            await XlyBuild.aio_update(validated_data=xly_build, params_data={"job_id": job_id})
               
