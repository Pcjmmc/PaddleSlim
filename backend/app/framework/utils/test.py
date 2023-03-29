#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

from xly import XlyOpenApiRequest

xly_agent = XlyOpenApiRequest()
url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipelines/getPipelineBuildPageUrl?pipelineBuildId=7950458"
url_param = "pipelineBuildId=7950458"
res = xly_agent.get_method(url,  param=url_param)


print(res.text)

