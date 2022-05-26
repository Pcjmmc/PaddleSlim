# !/usr/bin/env python3
"""
主要负责汇聚进展
"""
# encoding=utf-8
import time
from ce_web.settings.scenes import scenes_dict

class Summary(object):
    @classmethod
    def get_summary(cls, temp_data):
        """
        根据数据汇聚成想要的格式
        """
        init_sumary = {k: {
            "task_type": v,
            "status": "Passed",
            "total": 0,
            "failed": 0,
            "percent": 0,
            "undone": 0,
            "done": 0,
            "Passed": True
        } for k, v in scenes_dict.items()}
        # 如果有undone > 0; 则计算任务进度 undone / (undone+done)；且分类状态整体为undone
        # 如果undone = 0; 则修改任务状态有失败则失败，否则为成功
        for item in temp_data:
            task_type = item["task_type"]
            total_case = item["total_case"]
            failed_case = item["failed_case"]
            status = item["status"]
            if task_type == "compile":
                init_sumary[task_type]["total"] += 1
                if status and status.lower() == "failed":
                    init_sumary[task_type]["failed"] += 1
            else:
                init_sumary[task_type]["total"] += int(total_case)
                init_sumary[task_type]["failed"] += int(failed_case)
            if not status or status == "undone":
                # 记录下未完成的任务数
                init_sumary[task_type]["undone"] += 1
                # 同时将该类的结果标记成未完成
                init_sumary[task_type]["status"] = "undone"
            else:
                # 记录下已完成的数
                init_sumary[task_type]["done"] += 1
                # 如果有任务失败，则记录
                if status and status.lower() == "failed":
                    init_sumary[task_type]["Passed"] = False
        # 最后遍历完整合数据
        for k, v in init_sumary.items():
            status = v.get("status")
            # 优先记录undone；
            if status and status.lower() == "undone":
                try:
                    v["percent"] = int(v["done"] / (v["undone"] + v["done"]) * 100) 
                except:
                    v["percent"] = 0
            # 如果任务总数为0；即没有注册，则状态也是undone
            elif int((v["undone"] + v["done"])) == 0:
                v["status"] = "undone"
                try:
                    v["percent"] = int(v["done"] / (v["undone"] + v["done"]) * 100) 
                except:
                    v["percent"] = 0
            else:
                # 如果里面有任务失败则失败，不能根据case情况而定，假如有个任务失败了没有case；其他都成功了
                v["status"] = "Passed" if v["Passed"] else "Failed"

        summary = [v for k, v in init_sumary.items()]
        return summary
