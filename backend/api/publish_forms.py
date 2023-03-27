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
    tag = forms.CharField(label='tag', required=True)
    commit_id = forms.CharField(label='commit id', required=True)
    commit_time = forms.CharField(label='commit time', required=False)
    status = forms.CharField(label='状态', required=True)
    test_step = forms.CharField(label='测试步骤', required=True)
    job_id = forms.CharField(label='阶段的id', required=False)
    build_time = forms.CharField(label='启动时间', required=False)
    check_info = forms.JSONField(label='数据项', required=False)
