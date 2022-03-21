# !/usr/bin/env python3
# encoding: utf-8
"""
对外提供API逻辑，实现增删改查; 支持各种task_type 
"""
import datetime
import json
import time

from models.task_builds import CeTaskBuilds
from models.tasks import CeTasks

from views.base_view import MABaseView


class CaseDetailView(MABaseView):
    """
    对外提供case详情的入库逻辑；支持各种类型的接口 todo； 后期要兼容lite的迁移
    """
    pass
