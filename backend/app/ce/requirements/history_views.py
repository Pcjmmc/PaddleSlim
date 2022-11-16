# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import (
    RPC_SETTINGS, TC_BASE_URL, XLY_BASE_URL, XLY_BASE_URL2
)
from ce_web.settings.scenes import back_dict, inner_dict, scenes_dict, selects
from models.icafe import CeIcafe
from models.project import Project
from rpc.icafe import CreateCard, GetCards, ModifyCardStatus

from views.base_view import MABaseView

PADDLE_ICAFE_USER = RPC_SETTINGS['paddle_icafe']['username']
PADDLE_ICAFE_PASSD = RPC_SETTINGS['paddle_icafe']['password']
baseUrl = "https://console.cloud.baidu-int.com/devops/icafe/issue/{space}-{sequence}/show"


class ProjectHistory(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取icafe对应所有测试数据
        """
        query_params = {}
        icafe_id = kwargs.get("icafe_id", 1)
        if not icafe_id:
           return {}
        #优先支持RD查询所有卡片，并分页
        #其它字段可以按需支持比如卡片号
        query_params["icafe_id"] = icafe_id
        test_info_list = await Project().aio_filter_details(need_all=True, order_by="-created", group_by=None, **query_params)
        result_list = []
        for item in test_info_list:
            tmp_dict = {
                "test_id": item.get("test_id"),
                "test_status": item.get("test_status"),
                "approve": item.get("approve") if item.get("approve") else "",
                "created": item.get("created")
            }
            result_list.append(tmp_dict)
        print(result_list)
        return len(result_list), result_list

