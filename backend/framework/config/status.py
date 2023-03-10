#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
#
"""
用来定义错误代码和信息
"""



ERROR_133 = "module name error, can not support this test module yet!"
ERROR_233 = "mission name error, check mission code"
ERROR_600 = "下载报告解压出错"
ERROR_601 = "allure报告生成失败"
ERROR_602 = "数据库写入失败"
ERROR_800 = "效率云触发任务失败，请检查效率云接口"


class MissionStatus(object):
    """
    常量
    """
    # 测试任务状态
    ERROR = "error"
    RUNNING = "running"
    DONE = "done"
    # 测试结果状态
    FAIL = "fail"
    SUCCESS = "success"


ERROR_MSG = {
    # 退出码： 退出码含义 （下面是示例）
    "600": "这是一个错误信息映射",
    "601": "这是另一个错误信息映射",
    "602": "这是另另一个错误信息映射",
    "603": "这是另另另一个错误信息映射",
}