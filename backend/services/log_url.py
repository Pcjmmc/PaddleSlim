"""
负责拼接xly或者tc的日志连接
"""
# encoding: utf-8
from ce_web.settings.common import (
    STORAGE, TC_BASE_URL, 
    XLY_BASE_URL, XLY_BASE_URL2
)
def get_log_url(platform, workspace, build_id, job_id=None, build_type_id=None):
    log_url = ""
    if platform == "xly":
        log_url = XLY_BASE_URL.format(
            workspace=workspace,
            build_id=build_id,
            job_id=job_id
        )  if job_id else XLY_BASE_URL2.format(
            workspace=workspace,
            build_id=build_id
        )
    elif platform == 'teamcity':
        log_url = TC_BASE_URL.format(
            build_id=build_id,
            build_type_id=build_type_id
        )

    return log_url