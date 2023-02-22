#!/bin/env python3
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

import asyncio
import json

from views.base_view import MABaseView
from models.framework import ReleaseDailySettings, ReleaseDailyContent
from exception import HTTP400Error
from datetime import datetime
from framework.dispatcher import Dispatcher
import requests
from operator import itemgetter


class ReportSummary(MABaseView):
    """
    生成报告
    """
    async def get(self, **kwargs):
        """
        get
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        get
        """
        settings = await self.get_report_settings()
        settings = sorted(settings, key=itemgetter("order"))
        data = {"settings": settings, "important": {}, "regression": {}, "content": [], "icafes": {}}
        for setting in settings:
            module_id = setting["id"]
            res = await ReleaseDailyContent.aio_filter_details(order_by="-create_time",
                                                               module_id=module_id, version=self._cookies.get("ver"))
            if len(res) == 0:
                continue
            else:
                res[0]["create_time"] = str(res[0]["create_time"])
                data["content"].append(res[0])
                # important 高阶风险处理
                imp = self.important(setting["module"], res[0]["content"])
                data["important"].update(imp)

                # regression 回测信息汇总
                reg = self.regression(setting["module"], res[0]["content"])
                data["regression"].update(reg)

                # icafes 卡片汇总
                icafe = self.icafes(setting["module"], res[0]["content"])
                data["icafes"].update(icafe)

        # summary get!
        data["important_summary"] = self.important_summary(data["content"])
        data["regression_summary"] = self.regression_summary(data["content"])
        return len(settings), data

    async def get_report_settings(self):
        """
        获取看板配置信息
        """
        return await ReleaseDailySettings.aio_filter_details(need_all=True)

    def important(self, module, content):
        """
        important 高阶风险处理汇总
        """
        data = {}
        # content 处理
        if isinstance(content, str):
            content = json.loads(content)
        for i in content.get("risk", []):
            if i.get("important") == "是" and i.get("status") == "未解决":
                # 判断如果有内容就append
                if data.get(module) is None:
                    data[module] = []
                i["owner"] = []
                for icafe in i.get("icafe"):
                    i["owner"] = i["owner"] + icafe.get("owner")
                i["owner"] = " @".join(i["owner"])
                data[module].append(i)
        return data

    def important_summary(self, content):
        """
        important 高阶风险处理汇总
        """
        data = {"未解决": 0, "已解决": 0, "延期": 0}
        # content 处理
        for i in content:
            if isinstance(i.get("content"), str):
                i = json.loads(i.get("content"))
            for risk in i.get("risk"):
                if risk.get("important") == "否":
                    continue
                status = risk.get("status")
                if status == "未解决":
                    data["未解决"] += 1
                elif status == "已解决":
                    data["已解决"] += 1
                else:
                    data["延期"] += 1
        data["总量"] = data["未解决"] + data["已解决"] + data["延期"]
        data["修复率"] = format(100, '.2%') if data["总量"] == 0 else format(data["已解决"] / data["总量"], '.2%')
        return data

    def regression(self, module, content):
        """
        regression 集测进展同步
        """
        data = {}
        # content 处理
        if isinstance(content, str):
            content = json.loads(content)
        reg = content.get("regression", None)
        if reg is not None:
            reg["progress"] = format(0, '.2%') if reg["total"] == 0 else format(reg["pass"] / reg["total"], '.2%')
        data[module] = reg
        return data

    def regression_summary(self, content):
        """
        regression 集测进展整体
        """
        data = {"total": 0, "pass": 0, "fail": 0, "running": 0}
        # content 处理
        for i in content:
            if isinstance(i.get("content"), str):
                i = json.loads(i.get("content"))
            reg = i.get("regression")
            data["total"] += int(reg["total"])
            data["pass"] += int(reg["pass"])
            data["fail"] += int(reg["fail"])
            data["running"] += int(reg["running"])
        data["progress"] = format(0, '.2%') if data["total"] == 0 else format(data["pass"] / data["total"], '.2%')
        return data

    def icafes(self, module, content):
        """
        regression 集测进展同步
        """
        data = {}
        # content 处理
        if isinstance(content, str):
            content = json.loads(content)
        icafe = content.get("icafe", None)
        data[module] = icafe
        return data