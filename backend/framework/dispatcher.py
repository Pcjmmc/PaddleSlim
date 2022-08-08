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
from framework.config.service_url import Local, LocalMission, Cloud, CloudMission, PLACE, CLOUD, LOCAL, DOCKER_IMAGE
import requests
import framework.config.status as STATUS
from framework.utils.xly import XlyOpenApiRequest


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
            pipelineid = module
            url_param = "pipelineId={}".format(pipelineid)
            # branch ciType commit 毛用没有
            params = {
                "id": str(id),
                "wheel": wheel,
                "python": json.loads(env).get("python"),
                "cuda": json.loads(env).get("cuda"),
                "env": str(json.loads(env)),
                "docker_image": DOCKER_IMAGE.get(json.loads(env).get("cuda"))
            }
            data = {
                "branch": "develop",
                "ciType": "MERGE",
                "params": json.dumps(params)
            }
            data = json.dumps(data)
            print(data)
            url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipeline-builds?pipelineId={}".format(pipelineid)
            res = xly_agent.post_method(url, data, param=url_param)
            if res.status_code != 200:
                print(res.json())
                raise HTTP400Error
            else:
                print(res.json())
                return True

    @classmethod
    def local_run(cls):
        # todo: 本地化执行
        # res = requests.post(Local.API_FUNCTION)
        # if res.json().get("code") == 200:
        #     return True
        # else:
        #     return False
        pass

    @classmethod
    def request_mission(self, module, id, env, wheel):
        # todo: 请求任务 任务环境，编译内容，发送请求给效率云
        if PLACE.get(module) is not None:
            if PLACE.get(module) == CLOUD:
                # todo: 效率云的请求发送
                return self.cloud_run(CloudMission.ROUTER.get(module), id, env, wheel)
            elif PLACE.get(module) == LOCAL:
                # todo: 本地化部署
                pass
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
        mission = json.loads(job.get("mission"))
        res = await Compile.aio_get_object(order_by=None, group_by=None, id=job.get("compile"))
        wheel = res["wheel"]
        env = res["env"]
        retry_time = 5
        for k, v in mission.items():
            # if v is not None:
            #     continue
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
                if res is True:
                    # todo:初始化任务
                    await Mission.aio_update({"status": "running"}, {"id":id})
                    break
                else:
                    await Mission.aio_update({"status": res}, {"id": id})
                    retry += 1
        await Job.aio_update({"mission": str(json.dumps(mission))}, {"id":job.get("id")})


