#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

import asyncio
import json

from views.base_view import MABaseView
from models.framework import ReleaseDailySettings, ReleaseDailyContent
from framework.config.release_daily_settings import RELEASE_DAILY_SUPERUSER
from models.user import User
from exception import HTTP400Error
from datetime import datetime
from framework.dispatcher import Dispatcher
import requests


class ReportAdd(MABaseView):
    """
    天级报告展示
    """
    async def post(self, **kwargs):
        """
        post
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        获取数据
        """
        module_id = kwargs.get("module_id")
        content = kwargs.get("content")
        # content 处理
        if isinstance(content, str):
            content = json.loads(content)
        content = self.content_trans(content)
        release_daily_settings = await ReleaseDailySettings.aio_filter_details(id=module_id)
        print(release_daily_settings)
        owner = release_daily_settings[0]["owner"].split(",")
        module_name = release_daily_settings[0]["module"]
        uid = self._cookies.get("userid", 2) # 调试完需要改回来 0值
        # 查询用户名
        if uid == 0:
            raise HTTP400Error("未登录用户不能提交")
        else:
            user = await User.aio_filter_details(id=uid)
            if len(user) == 0:
                raise HTTP400Error("游客用户不能提交")
            else:
                username = user[0]["username"]
                if username != self._cookies.get("username"):
                    # 防止自行修改cookie
                    raise HTTP400Error("请勿自行修改cookie设置，操作禁止！")
                if username in owner or username in RELEASE_DAILY_SUPERUSER:
                    # 执行写入逻辑
                    data = {}
                    data["module_id"] = module_id
                    data["content"] = content
                    data["user"] = username
                    data["version"] = self._cookies.get("ver", "develop")
                    data["create_time"] = datetime.now()
                    res = await ReleaseDailyContent.aio_insert(data)
                    if res[0] == 0:
                        raise HTTP400Error("插入数据库失败，疑似数据库链接问题")
                else:
                    raise HTTP400Error("当前用户权限不能提交{}方向报告".format(module_name))
        return "数据写入成功"

    def content_trans(self, content):
        """
        json信息内容转换
        """

        risks = content.get("risk", None)
        regression = content.get("regression", None)
        content["icafe"] = []
        if risks is None or regression is None:
            raise HTTP400Error("提交数据格式错误")
        for i in range(len(risks)):
            icafes = risks[i].get("icafe", None)
            if icafes is None:
                continue
            else:
                for icafe in icafes:
                    icafe["ref"] = i
                    content["icafe"].append(icafe)
        # print(content)
        return str(json.dumps(content))








