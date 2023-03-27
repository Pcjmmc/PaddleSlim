# !/usr/bin/env python3
# encoding: utf-8
"""
view基类，实现get、post、put等基础查询
"""
import asyncio
import copy
import json
import urllib
import tornado.web
from exception import HTTP400Error, HTTP401Error, HTTP404Error, HTTPDetailError
from https import response as resp
from logger.decorator import BaseLoggerInfo

class BaseView(tornado.web.RequestHandler):
    """
    定义基类view
    """
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE, HEAD")

    def initialize(self, controller=None):
        """
        初始化（请求开始）
        """
        self.db_engines = self.application.db_engines

        self.model_classes = self.settings['model_classes']

        self.controller = controller

# method: get return list
class MABaseView(BaseView):
    """
    MABaseView 基类主要是对请求的封装，
    如需要在请求前做数据类型校验、健全等就可以在基类中实现，避免代码的重复构建
    实现发版记录的增删改查操作
    get: 获取数据
    put: 修改数据
    delete: 删除数据
    post: 创建数据
    """
    auth_class = None
    model_class = None
    post_form_class = None
    get_form_class = None
    put_form_class = None
    delete_form_class = None

    async def get_data(self, **kwargs):
        """
        调用子类get_data方法，真正实现数据获取的逻辑
        """
        return self.model_class.filter_object(**kwargs)

    def is_request_data_valid(self, **kwargs):
        """
        验证请求参数是否符合要求，可以后期接入django的 From模块
        """
        return True, None
    @property
    def _body_data(self):
        body_data = self.request.body
        if not body_data:
            return {}
        try:
            body_data = json.loads(body_data)
        except:
            body_data = {}
        return body_data
    
    @property
    def _cache_cookies(self):
        _cache_cookies = {}
        cache_cookies = {}
        if hasattr(self.request, 'cache_cookies'):
            _cache_cookies = self.request.cache_cookies
            for name in _cache_cookies:
                cache_cookies['_cookie_%s' % name] = _cache_cookies[name]
        return cache_cookies
    
    @property
    def headers(self):
        return self.request.headers

    @property
    def _cookies(self):
        _cookies = {}
        cookies = {}
        if hasattr(self.request, 'cookies'):
            _cookies = self.request.cookies
        for name in _cookies:
            cookies[name] = self.get_cookie(name)
        return cookies
    
    @property
    def request_data(self):
        form_data = {name: self.get_argument(name) for name in self.request.arguments}
        body_data = self._body_data
        request_data = {}
        request_data_temp = dict(**body_data, **form_data)
        request_data.update(request_data_temp)
        # 前端的bool是字符串
        for key in request_data:
            val = request_data[key]
            if val and str(val) == 'true':
                request_data[key] = True
            elif val and str(val) == 'false':
                request_data[key] = False

        return request_data

    def get_perfect_request_data(self):
        """
        解析和处理request的参数
        """
        return self.request_data
    @BaseLoggerInfo
    async def get(self):
        """
        重写get方法
        """
        # 如果校验没有登录则直接跳转
        try:
            if self.auth_class:
                need_redirect, sed_params = await self.auth_class.check_auth(self._cookies, self.headers)
                if need_redirect:
                    # 返回正常，让前端重新location
                    return resp.return_redirect_response(self, resp.HTTP_4001_INTERNAL_SERVER_ERROR, new_url=sed_params)
                else:
                    # 将user info种植到cookie中
                    username = sed_params.get("username")
                    self.set_cookie('username', username)
            kwargs = self.get_perfect_request_data()
            if self.get_form_class:
                form = self.get_form_class(kwargs)
                if not form.is_valid():
                    return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, form.errors)
            all_count, data = await self.get_data(**kwargs)
        except HTTP400Error as e:
            return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, e.error_message)
        except HTTP401Error as e:
            return resp.return_error_response(self, resp.HTTP_401_BAD_REQUEST, e.error_message)
        except HTTP404Error as e:
            return resp.return_error_response(self, resp.HTTP_404_NOT_FOUND, e.error_message)
        return resp.return_success_response(self, data=data, all_count=all_count)


    async def post_data(self, **kwargs):
        return self.model_class.get_object(**kwargs)
    
    @BaseLoggerInfo
    async def post(self, **kwargs):
        """
        父类post调用子类的post_data, 实现真正的逻辑
        """
        try:
            if self.auth_class:
                need_redirect, sed_params = await self.auth_class.check_auth(self._cookies, self.headers)
                if need_redirect:
                    # 返回正常，让前端重新location
                    return resp.return_redirect_response(self, resp.HTTP_4001_INTERNAL_SERVER_ERROR, new_url=sed_params)
                else:
                    # 将user info种植到cookie中
                    username = sed_params.get("username")
                    self.set_cookie('username', username)
            kwargs = self.get_perfect_request_data()
            if self.post_form_class:
                form = self.post_form_class(kwargs)
                if not form.is_valid():
                    return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, form.errors)
            data = await self.post_data(**kwargs)
        except HTTP400Error as e:
            return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, e.error_message)
        except HTTP401Error as e:
            return resp.return_error_response(self, resp.HTTP_401_BAD_REQUEST, e.error_message)
        except HTTPDetailError as e:
            return resp.response(self, e.error_detail)
        
        return resp.return_success_response(self, data)

    async def put_data(self, **kwargs):
        return self.model_class.get_object(**kwargs)

    @BaseLoggerInfo
    async def put(self, **kwargs):
        # 在数据处理之前可以嵌入django form表单的参数校验
        try:
            if self.auth_class:
                need_redirect, sed_params = await self.auth_class.check_auth(self._cookies, self.headers)
                if need_redirect:
                    # 返回正常，让前端重新location
                    return resp.return_redirect_response(self, resp.HTTP_4001_INTERNAL_SERVER_ERROR, new_url=sed_params)
                else:
                    # 将user info种植到cookie中
                    username = sed_params.get("username")
                    self.set_cookie('username', username)
            kwargs = self.get_perfect_request_data()
            if self.put_form_class:
                form = self.put_form_class(kwargs)
                if not form.is_valid():
                    return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, form.errors)
            data = await self.put_data(**kwargs)
        except HTTP400Error as e:
            return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, e.error_message)
        except HTTP401Error as e:
            return resp.return_error_response(self, resp.HTTP_401_BAD_REQUEST, e.error_message)
        except HTTPDetailError as e:
            return resp.response(self, e.error_detail)
        
        return resp.return_success_response(self, data)

    async def delete_data(self, **kwargs):
        return self.model_class.get_object(**kwargs)

    @BaseLoggerInfo
    async def delete(self, **kwargs):
        try:
            if self.auth_class:
                need_redirect, sed_params = await self.auth_class.check_auth(self._cookies, self.headers)
                if need_redirect:
                    # 返回正常，让前端重新location
                    return resp.return_redirect_response(self, resp.HTTP_4001_INTERNAL_SERVER_ERROR, new_url=sed_params)
                else:
                    # 将user info种植到cookie中
                    username = sed_params.get("username")
                    self.set_cookie('username', username)
            kwargs = self.get_perfect_request_data()
            if self.delete_form_class:
                form = self.delete_form_class(kwargs)
                if not form.is_valid():
                    return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, form.errors)
            data = await self.delete_data(**kwargs)
        except HTTP400Error as e:
            return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, e.error_message)
        except HTTP401Error as e:
            return resp.return_error_response(self, resp.HTTP_401_BAD_REQUEST, e.error_message)
        except HTTPDetailError as e:
            return resp.response(self, e.error_detail)
        
        return resp.return_success_response(self, data)
        
