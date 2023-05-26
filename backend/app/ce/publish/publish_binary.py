# !/usr/bin/env python3
# encoding: utf-8
"""
对内提供二分查找信息的快速存储
"""
from models.binary_search_status import BinarySearchStatus
from views.base_view import MABaseView
import time

class PublishBinary(MABaseView):


    async def get(self, **kwargs):
        return await super().get(**kwargs)
    
    """
    入参：
        email
        model_name是固定值
        step_name不是固定值
        tag_name不是固定值
    返回值：
        按照step_name
    """
    async def get_data(self, **kwargs):
        data =  await BinarySearchStatus.aio_filter_details(order_by='-updated', group_by=None, **kwargs)
        res =  {}
        for item in data:
            step_name = item['step_name']
            tag_name = item['tag_name']
            if (step_name in res):
                step =  res[step_name]
            else:
                step = {}
                res[step_name] = step
            if (tag_name not in step):
                updeted =  item['updated']
                now = int(time.time())
                days = (now - updeted) // 86400
                if (days > 10): # 超过10天，存储空的对象
                    res[step_name][tag_name] = None
                else: # 不超过10天，存储新的对象
                    json = {}
                    json['xly_link'] = item['xly_link']
                    json['status'] = item['status']
                    res[step_name][tag_name] = json
        return 1, res