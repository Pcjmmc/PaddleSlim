#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import json

from views.base_view import MABaseView
from models.framework import Job, Mission, Compile
from datetime import datetime
from app.framework.dispatcher import Dispatcher
from app.framework.config.service_url import COMPILE_SERVICE
import requests
import requests
import app.framework.config.status as STATUS
from app.framework.utils.xly import get_xly_mission_url
from app.framework.config.service_url import Local, LocalMission, Cloud, CloudMission, PLACE, CLOUD, LOCAL, DOCKER_IMAGE, DOCKER_INFER_IMAGE



class MissionRerun(MABaseView):
    """
    手动标记任务失败
    """
    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        快速失败
        """
        # 获取mission数据
        mission_id = kwargs.get("id")
        mission_info = await Mission.aio_get_object(id=mission_id)
        mission_name = mission_info["module"]
        # 获取环境数据
        jid = mission_info["jid"]
        job_info = await Job.aio_get_object(id=jid)
        compile_info = await Compile.aio_get_object(order_by=None, group_by=None, id=job_info["compile"])
        wheel = compile_info["wheel"]
        env = compile_info["env"]

        # 触发任务
        retry = 0
        retry_time = 5
        while (retry < retry_time):
            res = Dispatcher.request_mission(mission_name, mission_id, env, wheel)
            if isinstance(res, dict):
                # 初始化任务 获取效率云链接
                if PLACE.get(mission_name) == CLOUD:
                    info = get_xly_mission_url(res.get("pipelineBuildId"))
                    print(info)
                    await Mission.aio_update({"status": "running", "description": res.get("pipelineBuildId"),
                                              "info": info, "result": "", "allure_report":"", "bos_url": ""},
                                             {"id":mission_id})
                    await Job.aio_update({"status": "running"}, {"id": jid})
                    return "重新执行成功"
                elif PLACE.get(mission_name) == LOCAL:
                    await Mission.aio_update({"status": "running"}, {"id": mission_id})
                    return "重新执行成功"
                else:
                    return STATUS.ERROR_233
            else:
                await Mission.aio_update({"status": "error", "description": res}, {"id": mission_id})
                retry += 1
        # 如果重试超时，定义主任务是异常状态
        if retry == 5:
            await Job.aio_update({"status": "error"}, {"id": jid})
        return "重新执行失败"



    #
    #
    #
    #
    # @classmethod
    # def cloud_run(cls, module, id, env, wheel):
    #     if isinstance(module, list):
    #         for m in module:
    #             cls.cloud_run(CloudMission.ROUTER.get(m), id, env, wheel)
    #     else:
    #         xly_agent = XlyOpenApiRequest()
    #         # tuple structure for some special missions must need only one pipeline
    #         pipelineid = module[0] if isinstance(module, tuple) else module
    #         spec_param = module[1] if isinstance(module, tuple) else {}
    #         url_param = "pipelineId={}".format(pipelineid)
    #         # branch ciType commit 毛用没有
    #         params = {
    #             "id": str(id),
    #             "wheel": wheel,
    #             "python": json.loads(env).get("python"),
    #             "cuda": json.loads(env).get("cuda"),
    #             "env": str(json.loads(env)),
    #             "docker_image": DOCKER_IMAGE.get(json.loads(env).get("cuda")),
    #             "docker_infer_image": DOCKER_INFER_IMAGE.get(json.loads(env).get("cuda"))
    #         }
    #         total_param = dict(spec_param, **params)
    #         data = {
    #             "branch": "develop",
    #             "ciType": "MERGE",
    #             "params": json.dumps(total_param)
    #         }
    #         data = json.dumps(data)
    #         url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipeline-builds?pipelineId={}".format(pipelineid)
    #         res = xly_agent.post_method(url, data, param=url_param)
    #         if res.status_code != 200:
    #             print(res)
    #             print(res.content.decode('utf-8'))
    #             return STATUS.ERROR_800 + "错误码：" + str(res.status_code) + res.content.decode('utf-8')
    #         else:
    #             print(res.json())
    #             return res.json()
    #
    # @classmethod
    # def local_run(cls, module, id, env, wheel, mission):
    #     """
    #     module 是具体模块和参数
    #     id 是任务id
    #     env 是 环境
    #     wheel 是 包地址
    #     mission是 任务名字
    #     """
    #     # todo: 本地化执行
    #     if isinstance(module, list):
    #         for m in module:
    #             cls.local_run(CloudMission.ROUTER.get(m), id, env, wheel)
    #     else:
    #         # 为benchmark专门搞参数对应
    #         if "models_benchmark" in mission:
    #             service_url = module[0] if isinstance(module, tuple) else module
    #             spec_param = module[1] if isinstance(module, tuple) else {}
    #             params = {
    #                 "serviceId": "PTSservice_" + str(id),
    #                 "paddle_whl": wheel,
    #                 "python_version": json.loads(env).get("python").replace("python", ""),
    #                 "cuda_version": json.loads(env).get("cuda").replace("v", ""),
    #                 "email_address": "guomengmeng01@baidu.com,guolixin@baidu.com",
    #                 "branch": json.loads(env).get("branch"),
    #                 "type": json.loads(env).get("type"),
    #                 "type_value": json.loads(env).get("value"),
    #             }
    #             total_param = dict(spec_param, **params)
    #             res = requests.post(service_url, data=total_param)
    #             if res.status_code != 200:
    #                 return STATUS.ERROR_800
    #             else:
    #                 print(res.json())
    #                 return res.json()
    #
    # @classmethod
    # def request_mission(self, module, id, env, wheel):
    #     # todo: 请求任务 任务环境，编译内容，发送请求给效率云
    #     if PLACE.get(module) is not None:
    #         if PLACE.get(module) == CLOUD:
    #             # todo: 效率云的请求发送
    #             return self.cloud_run(CloudMission.ROUTER.get(module), id, env, wheel)
    #         elif PLACE.get(module) == LOCAL:
    #             # todo: 本地化部署
    #             return self.local_run(LocalMission.ROUTER.get(module), id, env, wheel, module)
    #         else:
    #             return STATUS.ERROR_233
    #     else:
    #         # todo: 其他策略
    #         return STATUS.ERROR_133





