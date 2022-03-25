# -*- coding: utf-8 -*-
"""
icafe api
"""

import json
import sys
import requests
import codecs
API_URL_ADRESS = 'http://icafeapi.baidu-int.com'
HEADERS ={"Content-type": "application/json"}
#TODO 后续切换为paddle_qa账户
USERNAME = 'guozhengxin'
PASSWORD = 'VVV%2BdDWPFIUxRM%2FMXvKGwnacLKbp7svNGiZ'
 
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
class IcafeAPI():
    """
    Icafe API
    """
    @staticmethod
    def create_card(space, **args):
         url = "{}/api/v2/space/{}/issue/new".format(API_URL_ADRESS, space)
         issue = args["issue"]
         params = {
             "username": USERNAME,
             "password": PASSWORD,
             "issues": [ issue ],
         }
         
       
         data = json.dumps(params)
         try:
             #print('url[%s] data[%s]' %(url, data))
             resp = requests.post(url, data, headers=HEADERS)
             print(resp.text)
             resp.raise_for_status()
         except Exception as e:
             print("error")
             print(str(e))
             return False
         return True
   
    @staticmethod
    def get_card(space, iql):
        resp_data = {}
        url = "{}/api/spaces/{}/cards?u={}&pw={}&iql={}".format(API_URL_ADRESS, space, USERNAME, PASSWORD,iql)
        try: 
            print('url [%s]' %url)
            resp = requests.get(url=url, headers=HEADERS) 
            resp.raise_for_status()
            resp_data = resp.json()
            print('resp_data[%s]' %resp_data)
        except Exception as e:
            print(str(e))
        return resp_data

if __name__ == '__main__':
    issue = {
        "title": "测试自动建卡片",
        "type": "Bug",
        "detail": "测试内容",
        "fields": {
            "QA负责人": "guozhengxin",
            "流程状态": "新建",
            "auto_tag": "auto_bug"
            },
        "creator": "guozhengxin"
       } 
    #IcafeAPI.create_card("DLTP", issue=issue)
    IcafeAPI.get_card("DLTP", iql="auto_tag = auto_bug AND 类型 = Bug")
