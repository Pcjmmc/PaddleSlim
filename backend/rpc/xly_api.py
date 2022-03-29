#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
xly api 集合
"""

import requests
import json
import sys
from xly_open import XlyOpenApiRequest

class XlyApi():
    """
    xly api 
    触发，查询，取消任务
    """
    @staticmethod
    def run_job(pipelineid, branch, ciType, commit, diy_params=None):
        """
        触发xly流水线
        """
        url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipeline-builds?pipelineId={}".format(pipelineid)
        #需要加密参数
        param = 'pipelineId=%s' % pipelineid
        data = dict()
        headers = { "Content-Type": "application/json",
                     "IPIPE-UID": "Paddle-bot"
         }
        data['branch'] = branch
        data['ciType'] = ciType
        data['params'] = json.dumps(diy_params)
        json_data = json.dumps(data)
        res = XlyOpenApiRequest().post_method(url, json_data, param, headers=headers)
        return res
     
    @staticmethod
    def get_job(pipelinebuildid):
        """
        依据构建id获取流水线构建详情
        """
        url = "https://xly.bce.baidu.com/open-api/ipipe/agile/pipeline/v1/pipelineBuild/{}".format(pipelinebuildid)
        print("url=", url)
        headers = { "Content-Type": "application/json",
                     "IPIPE-UID": "Paddle-bot"
         }
        res = XlyOpenApiRequest().get_method(url, headers=headers)
        #print(res.json())
        print(res)
        return res
        
         

if __name__ == '__main__':
     pipelineid = "22094"
     branch =  "develop"
     ciType = "MERGE"
     commit ="93a2f5652fa632e4eff8febf49304d64ec72b569"
     diy_params = {"IPIPE_WHL_PATH":"hello"}
     #XlyApi().run_job(pipelineid, branch, ciType, commit, diy_params)
     XlyApi().get_job(5248008)
