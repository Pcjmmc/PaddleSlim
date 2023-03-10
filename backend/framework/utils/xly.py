"""
docstring
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# copy from  https://github.com/PaddlePaddle/Paddle-bot/blob/master/webservice/utils/auth_ipipe.py
import requests
import base64
import rsa
import json
import hashlib
import os

access_id = "4f93954b-75c9-4629-b053-c4bcc9f74eab"
serect = '''-----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEfHbv2jtSj5/+tpBmNdBU7x01WQg2h0R7ys1OVQUTnxDruz0Yd0S3zanJ1E9hPf5ek9NO8m8vXq7nHgc/uSGr2waezL4vxQdRw1oTlU4k/aX/imiEOO+1z7brJqNmQcOvziDwHqtnjl9lEkF05/Sp9W/y2Fb0+dTvv36jFSPwxwIDAQAB
        -----END PUBLIC KEY-----'''

class XlyAuthorization(object):
    """
    效率云认证
    """

    def __init__(self):
        """
        comment
        """
        self.access_id = "4f93954b-75c9-4629-b053-c4bcc9f74eab"
        self.serect = '''-----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEfHbv2jtSj5/+tpBmNdBU7x01WQg2h0R7ys1OVQUTnxDruz0Yd0S3zanJ1E9hPf5ek9NO8m8vXq7nHgc/uSGr2waezL4vxQdRw1oTlU4k/aX/imiEOO+1z7brJqNmQcOvziDwHqtnjl9lEkF05/Sp9W/y2Fb0+dTvv36jFSPwxwIDAQAB
        -----END PUBLIC KEY-----'''
        self.session = requests.Session()

    def encrypt(self, pub, original_text):
        """公钥加密"""
        pub = rsa.PublicKey.load_pkcs1_openssl_pem(pub)
        crypt_text = rsa.encrypt(bytes(original_text.encode('utf-8')), pub)
        return crypt_text  # 加密后的密文

    def query_2_md5(self, param):
        """
                comment
        """
        m = hashlib.md5()
        m.update(bytes(param.encode('utf-8')))
        dig = m.hexdigest()
        return dig

    def set_sign(self, param):
        """
                comment
        """
        dig = self.query_2_md5(param)
        auth_string = self.encrypt(self.serect, dig)
        cipher_text = base64.b64encode(auth_string)
        cipher_str = str(cipher_text, encoding="utf-8")
        sign = "%s %s" % (self.access_id, cipher_str)
        return sign


class XlyOpenApiRequest(XlyAuthorization):
    """请求xly的openAPI"""
    def get_method(self,
                   url,
                   param='',
                   headers={"Content-Type": "application/json", "IPIPE-UID": "5fd96836b50a463186a04dd7bbfb94a4"}):
        """
        xly get http
        """
        req = requests.Request("GET", url, headers=headers).prepare()
        sign = self.set_sign(param)
        req.headers.update({'Authorization': sign})
        res = self.session.send(req, timeout=30)
        return res

    def post_method(self,
                    url,
                    data,
                    param='',
                    headers={"Content-Type": "application/json", "IPIPE-UID": "5fd96836b50a463186a04dd7bbfb94a4"}):
        """
        xly post http
        """
        req = requests.Request(
            "POST", url, data=data, headers=headers).prepare()
        sign = self.set_sign(param)
        req.headers.update({'Authorization': sign})
        res = self.session.send(req, timeout=15)
        return res


def encrypt(pub, original_text):  # 用公钥加密
    """
            comment
    """
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(pub)
    crypt_text = rsa.encrypt(bytes(original_text.encode('utf-8')), pub)
    return crypt_text  # 加密后的密文


def query_2_md5(query_param):
    """
            comment
    """
    m = hashlib.md5()
    m.update(bytes(query_param.encode('utf-8')))
    dig = m.hexdigest()
    return dig


def Sign(query_param):
    """
            comment
    """
    dig = query_2_md5(query_param)
    auth_string = encrypt(serect, dig)
    cipher_text = base64.b64encode(auth_string)
    cipher_str = str(cipher_text, encoding="utf-8")
    sign = "%s %s" % (access_id, cipher_str)
    return sign


def Get_ipipe_auth(url, query_param=''):
    """
            comment
    """
    session = requests.Session()
    req = requests.Request(
        "GET", url, headers={"Content-Type": "application/json"}).prepare()
    sign = Sign(query_param)
    req.headers.update({'Authorization': sign})
    return session, req


def Post_ipipe_auth(url, data, query_param=''):
    """
            comment
    """
    session = requests.Session()
    req = requests.Request(
        "POST", url, data=data,
        headers={"Content-Type": "application/json"}).prepare()
    sign = Sign(query_param)
    req.headers.update({'Authorization': sign})
    return session, req


def get_xly_mission_url(pipelineBuildId):
    """
    获取效率云任务链接
    """
    retry = 0
    xly_agent = XlyOpenApiRequest()
    while (retry < 5):
        url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v3/pipelines/getPipelineBuildPageUrl?pipelineBuildId={}".format(pipelineBuildId)
        url_param = "pipelineBuildId={}".format(pipelineBuildId)
        res = xly_agent.get_method(url, param=url_param)
        if res.status_code == 200:
            res_str = res.text.replace("\"", "")
            return res_str
        else:
            retry += 1
    return None


def pipeline_cancel(pipelineBuildId):
    """
    取消流水线
    """
    retry = 0
    xly_agent = XlyOpenApiRequest()
    while (retry < 5):
        url = "https://xly.bce.baidu.com/open-api/ipipe/rest/v4/pipelines/{}/cancel".format(
            pipelineBuildId)
        data = '{"type":"CANCEL"}'
        res = xly_agent.post_method(url, data)
        if res.status_code == 200:
            return True
        else:
            retry += 1
    return False