#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile
from exception import HTTP400Error
from datetime import datetime
from app.framework.config.service_url import Local, LocalMission, Cloud, CloudMission, PLACE, CLOUD, LOCAL, DOCKER_IMAGE, DOCKER_INFER_IMAGE
import requests
import app.framework.config.status as STATUS
from app.framework.utils.xly import XlyOpenApiRequest, get_xly_mission_url


class Dispatcher(object):
    """
    调度器
    """
    @classmethod
    def cloud_run(cls, module, id, env, wheel):
        if isinstance(module, list):
            for m in module:
                cls.cloud_run(CloudMission.ROUTER.get(m), id, env, wheel)
        else:
            xly_agent = XlyOpenApiRequest()
            # tuple structure for some special missions must need only one pipeline
            pipelineid = module[0] if isinstance(module, tuple) else module
            spec_param = module[1] if isinstance(module, tuple) else {}
            url_param = "pipelineId={}".format(pipelineid)
            # branch ciType commit 毛用没有
            params = {
                "id": str(id),
                "wheel": wheel,
                "python": json.loads(env).get("python"),
                "cuda": json.loads(env).get("cuda"),
                "branch": json.loads(env).get("branch"),
                "env": str(json.loads(env)),
                "docker_image": DOCKER_IMAGE.get(json.loads(env).get("cuda")),
                "docker_infer_image": DOCKER_INFER_IMAGE.get(json.loads(env).get("cuda"))
            }
            total_param = dict(spec_param, **params)
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
    def local_run(cls, module, id, env, wheel, mission):
        """
        module 是具体模块和参数
        id 是任务id
        env 是 环境
        wheel 是 包地址
        mission是 任务名字
        """
        # todo: 本地化执行
        if isinstance(module, list):
            for m in module:
                cls.local_run(CloudMission.ROUTER.get(m), id, env, wheel)
        else:
            # 为benchmark专门搞参数对应
            if "models_benchmark" in mission:
                service_url = module[0] if isinstance(module, tuple) else module
                spec_param = module[1] if isinstance(module, tuple) else {}
                params = {
                    "serviceId": "PTSservice_" + str(id),
                    "paddle_whl": wheel,
                    "python_version": json.loads(env).get("python").replace("python", ""),
                    "cuda_version": json.loads(env).get("cuda").replace("v", ""),
                    "email_address": "guomengmeng01@baidu.com,guolixin@baidu.com",
                    "branch": json.loads(env).get("branch"),
                    "type": json.loads(env).get("type"),
                    "type_value": json.loads(env).get("value"),
                }
                total_param = dict(spec_param, **params)
                res = requests.post(service_url, data=total_param)
                if res.status_code != 200:
                    return STATUS.ERROR_800
                else:
                    print(res.json())
                    return res.json()
    @classmethod
    def request_mission(self, module, id, env, wheel):
        # todo: 请求任务 任务环境，编译内容，发送请求给效率云
        if PLACE.get(module) is not None:
            if PLACE.get(module) == CLOUD:
                # todo: 效率云的请求发送
                return self.cloud_run(CloudMission.ROUTER.get(module), id, env, wheel)
            elif PLACE.get(module) == LOCAL:
                # todo: 本地化部署
                return self.local_run(LocalMission.ROUTER.get(module), id, env, wheel, module)
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
        res = await Compile.aio_get_object(order_by=None, group_by=None, id=job.get("compile"))
        wheel = res["wheel"]
        env = res["env"]
        retry_time = 5
        for k, v in mission.items():
            # 如果任务有id，不继续触发。
            if v is not None:
                continue
            retry = 0
            data = {"jid": job.get("id"),
                    "status": "init",
                    "module": k,
                    "create_time": datetime.now(),
                    "update_time": datetime.now()},
            res = await Mission.aio_insert(data)
            if res[0] == 0:
                raise HTTP400Error
            id = res[1]
            mission[k] = id
            while(retry < retry_time):
                res = self.request_mission(k, id, env, wheel)
                if isinstance(res, dict):
                    # 初始化任务 获取效率云链接
                    if PLACE.get(k) == CLOUD:
                        info = get_xly_mission_url(res.get("pipelineBuildId"))
                        print(info)
                        await Mission.aio_update({"status": "running", "description": res.get("pipelineBuildId"),
                                                  "info": info}, {"id":id})
                        break
                    else:
                        await Mission.aio_update({"status": "running"}, {"id": id})
                else:
                    await Mission.aio_update({"status": "error", "description": res}, {"id": id})
                    retry += 1
        await Job.aio_update({"mission": str(json.dumps(mission))}, {"id":job.get("id")})

