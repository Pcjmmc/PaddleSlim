# !/usr/bin/env python3
# encoding: utf-8
"""
对外提供API逻辑，实现增删改查
"""
import asyncio
import json
import time
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
        #print(header)
        trigger_type = header.get("TRIGGER_TYPE", "")
        operation = header.get("OPERATION", "")
        status = header.get("BUILD_STATUS", "")
        mark_job = header.get("MARKED_JOB", "false")
        if mark_job == "true":
            return None
        xly_basic = {}
        xly_build = {}
        if "STATUS" == trigger_type and "PENDING" == status:
            xly_basic['conf_id'] = kwargs.get("conf_id")
            xly_basic['workspace'] = kwargs.get("workspace")
            xly_basic['jobname'] = kwargs.get("jobname")
            print(xly_basic)
            await XlyBasic.aio_insert(xly_basic)
            xly_build['build_id'] = kwargs.get("build_id")
            xly_build['job_id'] = kwargs.get("job_id")
            xly_build['conf_id'] = kwargs.get("conf_id")
            xly_build['status'] = status
            begin_time = kwargs.get("begin_time", None)
            if begin_time:
                print("generate begin time")
                begin_time = int(int(begin_time) / 1000)
            else:
                print("web hook header not have JOB_START_TIME")
                begin_time = int(time.time())
            xly_build['begin_time'] = begin_time
            print("xly build info is", xly_build)
            await XlyBuild.aio_insert(xly_build) 
        if "STATUS" == trigger_type and "RUNNING" == status:
            job_id = kwargs.get("job_id")
            xly_build['status'] = status
            #xly_build['job_id'] = kwargs.get("job_id")
            run_time = kwargs.get("run_time", None)
            if run_time:
                run_time = int(int(run_time) / 1000)
            else:
                print("web hook header not have JOB_REAL_START_TIME")
                run_time = int(time.time())
            xly_build['run_time'] = run_time
            print(status, "xly buidl info is", xly_build)
            await XlyBuild.aio_update(validated_data=xly_build, params_data={"job_id": job_id})
        if "STATUS" == trigger_type and status in ["FAIL", "SUCC", "CANCEL"]:
            job_id = kwargs.get("job_id")
            xly_build['status'] = status
            xly_build["exit_code"] = kwargs.get("JOB_EXIT_CODE", None)
            end_time = kwargs.get("end_time", None) 
            if end_time:
                end_time = int(int(end_time) / 1000) 
            else:
                end_time = int(time.time())
            xly_build["end_time"] = end_time
            print(status, "xly build info is", xly_build)
            #考虑到任务如果被重复触发buildid不变，但是jobid变化，设置jobid为主键
            await XlyBuild.aio_update(validated_data=xly_build, params_data={"job_id": job_id})
        if "OPERATION" == trigger_type and "BUILD_ISSUE" == operation:
            #TODO 修正xlywebhook中文编码异常，待讨论
            job_id = kwargs.get("job_id")
            print("job_id =", job_id)
            mark_info_json = kwargs.get("OPERATION_DATA")
            mark_info = mark_info_json.get("CATEGORY_LIST", [])
            mark_info_str = ';'.join(mark_info)
            print("xly issue mark info is", mark_info_str)
            print(trigger_type, "xly build info is", xly_build) 
            xly_build["fail_reason"] = mark_info_str
            print(status, "xly build info is", xly_build)
            await XlyBuild.aio_update(validated_data=xly_build, params_data={"job_id": job_id})
