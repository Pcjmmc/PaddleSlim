import asyncio
import time

from models.project import Project

async def update_pts_status(**kwargs):
    """
    ֧��ptsд��dbʱ��ͬ��д��������Է��������״̬
    """
    test_id = kwargs.get("test_id")
    origin_status = kwargs.get("test_status")
    validated_data = {}
    validated_data["test_id"] = test_id
    #��pts��ͨptsԭʼ״̬������ӳ�����
    #��ʱ���ó�2����Ϊ����
    validated_data['test_status'] = 2
    #validated_data['test_status'] = origin_status
    await Project.aio_update(
            validated_data=kwargs, params_data={"test_id" : test_id}
        )
    #TODO������֪rd/qa��ע

