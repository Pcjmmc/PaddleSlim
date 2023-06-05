#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  dispatcher.py
  * @author:  luozeyu01
  * @date  2023/3/30 7:43 PM
  * @brief
  *
  **************************************************************************/
"""

import asyncio
import json

from datetime import datetime
from exception import HTTP400Error
from models.fd_benchmark import Job, Mission
from app.fd_benchmark.config.service_url import Cloud, CloudMission, DOCKER_IMAGE, CLOUD, PLACE
from app.fd_benchmark.config.module import CompileParams
import app.fd_benchmark.config.status as STATUS
from app.fd_benchmark.utils.xly import XlyOpenApiRequest, get_xly_mission_url


class Dispatcher(object):
    """
    调度器
    """
    # def cloud_run(cls, module, id, fork, branch, compile_dict, bos_path):
    @classmethod
    def cloud_run(cls, hardware, comment, routine, uid, job_id, mission_id, fork, branch):
        """
        触发效率云
        """
        xly_agent = XlyOpenApiRequest()
        pipelineid = CloudMission.ROUTER.get(hardware)
        url_param = "pipelineId={}".format(pipelineid)
        # 构建效率云参数
        if hardware == 'gpu' or hardware == 'x86':
            params = {
                "comment": comment,
                "routine": str(routine),
                "uid": str(uid),
                "job_id": str(job_id),
                "mission_id": str(mission_id),
                "fork": fork,
                "branch": branch,
                # "bos_path": bos_path,
                "docker_image": DOCKER_IMAGE.get('v11.2'),
                "hardware": hardware,
            }
        else:
            params = {
                "comment": comment,
                "routine": str(routine),
                "uid": str(uid),
                "job_id": str(job_id),
                "mission_id": str(mission_id),
                "fork": fork,
                "branch": branch,
                # "bos_path": bos_path,
                "hardware": hardware,
            }
        # total_param = dict(params, **compile_dict)
        total_param = params
        data = {
            "branch": "develop",
            "ciType": "MERGE",
            "params": json.dumps(total_param)
        }
        data = json.dumps(data)
        url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipeline-builds?pipelineId={}".format(pipelineid)
        res = xly_agent.post_method(url, data, param=url_param)
        if res.status_code != 200:
            print(res)
            print(res.content.decode('utf-8'))
            return STATUS.ERROR_800 + "错误码：" + str(res.status_code) + res.content.decode('utf-8')
        else:
            print(res.json())
            return res.json()

    @classmethod
    def request_mission(self, hardware, comment, routine, uid, job_id, mission_id, fork, branch):
    # def request_mission(self, module, id, fork, branch, compile_dict, bos_path):
    # def request_mission(self, module, id, env, wheel):
        # todo: 请求任务 任务环境，编译内容，发送请求给效率云
        if PLACE.get(hardware) is not None:
            if PLACE.get(hardware) == CLOUD:
                # todo: 效率云的请求发送
                # return self.cloud_run(module, id, fork, branch, compile_dict, bos_path)
                return self.cloud_run(hardware, comment, routine, uid, job_id, mission_id, fork, branch)
            else:
                return STATUS.ERROR_233
        else:
            # todo: 其他策略
            return STATUS.ERROR_133

    @classmethod
    async def dispatch_missions(self, job):
        """
        任务分发器
        """
        # todo: 并行触发服务，初始化对应的服务数据
        if job.get("mission") is None:
            return "ok"
        mission = json.loads(job.get("mission"))
        # res = await Compile.aio_get_object(order_by=None, group_by=None, id=job.get("compile"))
        # wheel = res["wheel"]
        # env = res["env"]
        fork = job.get("fork")
        branch = job.get("branch")
        # bos_path = job.get("bos_path")
        retry_time = 5
        for k, v in mission.items():
            # 如果任务有id，不继续触发。
            if v is not None:
                continue
            retry = 0
            compile_dict = CompileParams.ROUTER.get(k)
            data = {"jid": job.get("id"),
                    "uid": job.get("uid"),
                    "status": "init",
                    "hardware": k,
                    "compile": str(compile_dict),
                    # "bos_path": bos_path + '/' + k + 'xls',
                    "create_time": datetime.now(),
                    "update_time": datetime.now()},
            res = await Mission.aio_insert(data)
            if res[0] == 0:
                raise HTTP400Error
            id = res[1]
            mission[k] = id

            while(retry < retry_time):
                # res = self.request_mission(k, id, env, wheel)
                # 输入示例 k='gpu', id='3', compile_dict={...}
                # res = self.request_mission(k, id, fork, branch, compile_dict, bos_path)
                res = self.request_mission(k, job.get("comment"), job.get("routine"), job.get("uid"), job.get("id"), id, fork, branch)
                if isinstance(res, dict):
                    # 初始化任务 获取效率云链接
                    if PLACE.get(k) == CLOUD:
                        info = get_xly_mission_url(res.get("pipelineBuildId"))
                        print(info)
                        await Mission.aio_update({"status": "running", "description": res.get("pipelineBuildId"),
                                                  "info": info}, {"id": id})
                        break
                    else:
                        return STATUS.ERROR_233
                else:
                    await Mission.aio_update({"status": "error", "description": res}, {"id": id})
                    retry += 1
            # 如果重试超时，定义主任务是异常状态
            if retry == 5:
                await Job.aio_update({"status": "error"}, {"id": job.get("id")})
        await Job.aio_update({"mission": str(json.dumps(mission))}, {"id":job.get("id")})
