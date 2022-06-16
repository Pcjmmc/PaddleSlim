# !/usr/bin/env python3
"""
负责op benchmark相关的增删改查等操作
"""
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.scenes import scenes_dict
from models.benchmark_cases import BenchmarkCases
from models.benchmark_jobs import BenchmarkJobs

from views.base_view import MABaseView


class BenchmarkManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        筛选策略，选出最新的1个job；拿到case详情
        """
        results = []
        result = await BenchmarkJobs.aio_get_object(
            order_by="-id"
        )
        jobid = result.id
        case_details = await BenchmarkCases.aio_filter_details(
            need_all=True, **{"jid": jobid}
        )
        details = [json.loads(item.get("result")) for item in case_details if item.get("result")]
        for item in details:
            tep = {}
            for key, value in item.items():
                if key != "yaml":
                    res = self.process_data(key, value)
                    tep.update(res)
                else:
                    tep.update({"yaml": value})
            results.append(tep)
        return len(results), results

    def process_data(self, key, value):
        res = {}
        for k, val in value.items():
            new_key = key + '_' + k
            res[new_key] = val
        return res