# !/usr/bin/env python3
# encoding: utf-8
"""
对外提供API逻辑，实现增删改查
"""
import asyncio
import json

from views.base_view import MABaseView


class TestView(MABaseView):
    """
    完成模型kpi的快速存储
    """

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        pass




