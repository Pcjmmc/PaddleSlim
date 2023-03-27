# encoding: utf-8
"""
自定义api的参数检验逻辑，比较简单
"""
from django import forms

class AddCaseForm(forms.Form):
    """
    定义接口接受的参数信息
    """
    build_type_id = forms.CharField(label='任务唯一id', required=True)
    build_id = forms.CharField(label='任务的编译id', required=True)
    repo = forms.CharField(label='仓库', required=True)
    branch = forms.CharField(label='分支', required=True)
    commit_id = forms.CharField(label='commit id', required=True)
    commit_time = forms.CharField(label='commit time', required=True)
    status = forms.CharField(label='状态', required=True)
    job_id = forms.CharField(label='阶段的id', required=False)
    build_time = forms.CharField(label='任务启动时间', required=False)
    left_time = forms.CharField(label='任务剩余时间', required=False)
    duration = forms.CharField(label='执行时长', required=False)
    case_detail = forms.JSONField(label='case信息', required=False)
    exit_code = forms.CharField(label='退出码', required=False)
