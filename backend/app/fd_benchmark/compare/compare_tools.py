#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
性能对比工具
"""

import asyncio
import json


def case_compare(latest_res, baseline_res):
    """

    :param res:
    :param exp:
    :return:
    """
    latest_return = {}
    baseline_return = {}
    compare_return = {}

    latest_dict = json.loads(latest_res)
    baseline_dict = json.loads(baseline_res)

    latest_keys = sorted(latest_dict.keys())
    baseline_keys = sorted(baseline_dict.keys())

    # if latest_keys != baseline_keys:
    #     return 1

    for index, value in latest_dict.items():
        if index in baseline_keys:
            if value == "" or value == "Failed":
                latest_return[index] = value
                baseline_return[index] = baseline_dict[index]
                compare_return[index] = value
                continue

            latest_return[index] = float(value)
            baseline_return[index] = float(baseline_dict[index])

            if float(value) == 0 or float(baseline_dict[index]) == 0:
                compare_return[index] = 0
            else:
                if float(value) > float(baseline_dict[index]):
                    compare_return[index] = (float(value) / float(baseline_dict[index])) * -1
                else:
                    compare_return[index] = float(baseline_dict[index]) / float(value)
        else:
            latest_return[index] = float(value)
            baseline_return[index] = 0
            compare_return[index] = 0

    return latest_return, baseline_return, compare_return
