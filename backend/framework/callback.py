import asyncio
import time

from models.project import Project

async def update_pts_status(**kwargs):
    """
    支持pts写回db时，同步写回需求测试服务关联表状态
    """
    test_id = kwargs.get("test_id")
    origin_status = kwargs.get("test_status")
    validated_data = {}
    validated_data["test_id"] = test_id
    #和pts沟通pts原始状态，并做映射入库
    #临时设置成2，作为测试
    validated_data['test_status'] = 2
    #validated_data['test_status'] = origin_status
    await Project.aio_update(
            validated_data=kwargs, params_data={"test_id" : test_id}
        )
    #TODO如流周知rd/qa关注

