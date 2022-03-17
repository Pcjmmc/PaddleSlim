# !/usr/bin/env python3
# encoding: utf-8
"""
定义ce 的taks表
"""
import asyncio
import os
import sys

import sqlalchemy as sa
from libs.mysql.db import BaseModel, BaseModelMixin, db_engines
from libs.mysql.schema import Column
from sqlalchemy import VARCHAR, BigInteger, Boolean, Column, Float, Integer, Text
from utils.md5 import get_md5


class CeTasks(BaseModel, BaseModelMixin):
    """
    定义tasks任务的表结构
    """
    __tablename__ = 'ce_task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tname = Column(VARCHAR(200), comment='任务名') # xly: ''; tc: %system.teamcity.buildConfName%
    # workspace = Column(VARCHAR(200), comment='所属的空间名') # xly：AGILE_WORKSPACE； tc:非必需，填写上一级的名字%system.teamcity.projectName% 
    owner = Column(VARCHAR(50), comment="任务所属人")
    build_type_id = Column(VARCHAR(255), comment="任务的build type") # xly： "pipelineConfId;得确定下这个值唯一吗"； teamcity："%system.teamcity.buildType.id%"
    platform = Column(VARCHAR(50), comment="任务所属平台") # tc or xly?
    system = Column(VARCHAR(50), comment="任务所属平台") # 测试的系统信息：Linux_gpu、T4、Xpu、 jetson、windows、mac等?
    description = Column(VARCHAR(100), comment="任务的概述") # 要求概述简单明了
    task_type = Column(VARCHAR(20), comment="任务的类型") #目前支持；model、frame、liet、infer、dist；这个主要是支持后期的特殊处理
    dependencies = Column(VARCHAR(100), comment="依赖的上游编译任务") # xly： "pipelineConfId;得确定下这个值唯一吗"； teamcity："%system.teamcity.buildType.id%"
    step = Column(VARCHAR(20), comment="任务所属的阶段") # compile: 编译任务； 下游任务有分成： develop； release；shared;
    created = Column(Integer, comment="本记录创建的时间")
    updated = Column(Integer, comment="本记录更新的时间")

    

    class Meta:
        """
        定义model属于那个库
        """
        app_label = 'ce'
    
    @classmethod
    async def create_or_update_task(cls, build_type, validated_data={}):
        """
        create record if not exist else update record
        根据params_data 来查询记录是否存在，注意必须可以唯一确定
        如果存在，则根据validated_data来更新记录
        如果不存在，则根据validated_data新建记录
        """
        tid = None
        params_data = {
            "build_type": get_md5(build_type),
            "build_type_id": build_type
        }
        result = await cls.aio_get_object(**params_data)
        if not result:
            _, tid = await cls.aio_insert(
                validated_data={
                    "pname": validated_data.get("pname"),
                    "tname": validated_data.get("tname"),
                    "owner": validated_data.get("owner"),
                    "build_type": params_data.get("build_type"),
                    "build_type_id": params_data.get("build_type_id"),
                    "platform": validated_data.get("platform"),
                    "step": validated_data.get("step")
                }
            )
        else:
            tid = result.id
            # 更新任务表信息
            await cls.aio_update(
            validated_data={
                "pname": validated_data.get("pname") or result.pname,
                "tname": validated_data.get("tname") or result.tname,
                "owner": validated_data.get("owner") or result.owner,
                "platform": validated_data.get("platform") or result.platform,
                "step": validated_data.get("step") or result.step,
            },
            params_data={"id": tid}
        )
        return tid

if __name__ == "__main__":
    # test insert
    loop =  asyncio.get_event_loop()
    params = {
        "tname": "test",
        "pname": "tbb3g3",
        "owner": "liuhuanling",
    }
    loop.run_until_complete(CeTask.aio_insert(validated_data=params))

