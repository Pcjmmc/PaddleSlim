# !/usr/bin/env python3
# encoding: utf-8
"""
对外提供API逻辑，实现增删改查
"""
import copy
from models.binary_search_status import BinarySearchStatus
from views.base_view import MABaseView


class PublishBinaryInfo(MABaseView):
    """
    完成binary信息的快速存储
    """

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        xly_id: 点击二分任务后所触发的效率云任务的id
        email: 在当前页面点击按钮的用户email
        xly_link: 点击二分任务后所触发的xly任务链接
        repo_name: 二分任务对应的repo_name
        model_name: 二分任务对应的model_name
        step_name: 二分任务对应的step_name
        tag_name: 二分任务对应的tag_name
        status: xly任务执行过程中返回的状态信息
        """
        xly_id = kwargs.get("xly_id")
        # binary task入库逻辑
        params = copy.deepcopy(kwargs)
        params.pop("xly_id")
        await BinarySearchStatus.create_or_update_build(
            xly_id, **params
        )
