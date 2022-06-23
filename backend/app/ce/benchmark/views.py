# !/usr/bin/env python3
"""
负责op benchmark相关的增删改查等操作
"""
import asyncio
import datetime
import json
import os
import shutil
import time
import urllib.request

# encoding=utf-8
import wget
import yaml
from ce_web.settings.common import PROJECT_ROOT, path
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
        results = {"job": {}, "case_detail": []}
        result = await BenchmarkJobs.aio_get_object(
            order_by="-id"
        )
        job = {key: val for key, val in result.items()}
        if job.get("update_time"):
            job["update_time"] = str(job.get("update_time"))
        if job.get("create_time"):
            job["create_time"] = str(job.get("create_time"))
        jobid = result.id
        results["job"] = job
        conf_dict = self.read_remote_yaml()
        #获取到即可删除
        self.delete_path()
        case_details = await BenchmarkCases.aio_filter_details(
            need_all=True, **{"jid": jobid}
        )
        details = [
            {"case_name": item.get("case_name"),
            "result_detail": json.loads(item.get("result"))}
            for item in case_details if item.get("result")
        ]
        for item in details:
            tep = {"case_name": item.get("case_name")}
            content = item.get("result_detail")
            for key, value in content.items():
                if key not in ["yaml"]:
                    res = self.process_data(key, value)
                    tep.update(res)
                else:
                    # 获取配置的具体信息
                    conf_detail = conf_dict.get(value, "")
                    tep.update({key: {"value": value, "conf_detail": conf_detail}})
            results["case_detail"].append(tep)
        return len(results), results

    def read_remote_yaml(self, url="https://raw.githubusercontent.com/PaddlePaddle/PaddleTest/develop/framework/e2e/yaml/test0.yml"):
        _, file_name = url.rsplit("/", 1)
        out = path(PROJECT_ROOT, "opBenchemarkConf")
        if not os.path.exists(out):
            # 不存在则创建路径
            os.makedirs(out)
        whl_file = path(out, file_name)
        # 判断下是否存在改文件存在则删除
        if file_name and os.path.exists(whl_file):
            os.remove(whl_file)
        wget.download(url, out=out)
        try:
            f = open(whl_file)
            store_dict = yaml.safe_load(f)
        except Exception as e:
            store_dict = {}
        finally:
            f.close()
        return store_dict

    def delete_path(self):
        out = path(PROJECT_ROOT, "opBenchemarkConf")
        if os.path.exists(out):
            shutil.rmtree(out)

    def process_data(self, key, value):
        res = {}
        for k, val in value.items():
            new_key = key + '_' + k
            try:
                # 如果可以转换成flaot型，则保留4位有效数字
                data = '%.4f' % (float(val))
                data = str(data)
            except:
                data = val
            res[new_key] = data
        return res
