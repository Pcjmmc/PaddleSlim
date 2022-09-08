"""
负责二分查找服务
"""
# !/usr/bin/env python3
# # encoding=utf-8
import asyncio
import base64
import datetime
import hashlib
import json
import os
import time

import requests
import rsa
from exception import HTTPDetailError

from views.base_view import MABaseView


class BinarySearchManage(MABaseView):

    async def post(self, **kwargs):
        """
        调用基类的post方法
        """
        return await super().post(**kwargs)


    async def post_data(self, **kwargs):
        """
        响应请求,根据条件实现二分查找
        """
        param='pipelineId=23574'
        access_id='4f93954b-75c9-4629-b053-c4bcc9f74eab'
        serect = '''-----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEfHbv2jtSj5/+tpBmNdBU7x01WQg2h0R7ys1
        OVQUTnxDruz0Yd0S3zanJ1E9hPf5ek9NO8m8vXq7nHgc/uSGr2waezL4vxQdRw1oTlU4k/aX/im
        iEOO+1z7brJqNmQcOvziDwHqtnjl9lEkF05/Sp9W/y2Fb0+dTvv36jFSPwxwIDAQAB
        -----END PUBLIC KEY-----'''
        sign = Sign(param, serect, access_id)
        url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipeline-builds?pipelineId=23574"
        new_params_json = json.dumps(kwargs)
        data = {
            "branch": "develop",
            "commit": "b1871ad36b8bf7434f3155738a999fba2f4585e6",
            "ciType": "MERGE",
            "params": new_params_json
            }
        json_data = json.dumps(data)
        req = requests.Request("POST", url, data=json_data, headers={"Content-Type": "application/json",
        "IPIPE-UID": "Paddle-bot"}).prepare()
        req.headers.update({'Authorization': sign})
        session =  requests.Session()
        res = session.send(req, timeout=15)
        if res.status_code == 200:
            content = json.loads(res.text)
            url = "https://xly.bce.baidu.com/paddlepaddle/PR-Location/newipipe/detail/{buildId}"
            url = url.format(buildId=content.get("pipelineBuildId"))
            data = {"url": url}
        else:
            raise HTTPDetailError(
                error_message="xly service error",
                error_detail={"code": 500, "message": "xly service error"}
            )
        return data
        

def encrypt(pub, original_text):  # 用公钥加密
    """
    encrypt
    """
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(pub)
    crypt_text = rsa.encrypt(bytes(original_text.encode('utf-8')), pub)
    return crypt_text  # 加密后的密文


def query_2_md5(query_param):
    """
    to md5
    """
    m = hashlib.md5()
    m.update(bytes(query_param.encode('utf-8')))
    dig = m.hexdigest()
    return dig


def Sign(query_param, serect, access_id):
    """
    build sign
    """
    dig = query_2_md5(query_param)
    auth_string = encrypt(serect, dig)
    cipher_text = base64.b64encode(auth_string)
    cipher_str = str(cipher_text, encoding="utf-8")
    sign = "%s %s" % (access_id, cipher_str)
    return sign

