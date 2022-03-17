# !/usr/bin/env python3
# encoding: utf-8
"""
view基类，实现get、post、put等基础查询
"""
import asyncio
import copy
import json

import tornado.web
from exception import HTTP400Error, HTTP404Error, HTTPDetailError
from https import response as resp


class BaseView(tornado.web.RequestHandler):
    """
    定义基类view
    """
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
    model_class = None

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
        body_data = self.request.body.decode('utf8')
        if not body_data:
            return {}
        try:
            body_data = json.loads(body_data)
        except:
            body_data = {}
        print('body data', body_data)
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
    def _cookies(self):
        _cookies = {}
        cookies = {}
        if hasattr(self.request, 'cache_cookies'):
            _cookies = self.request.cookies
        for name in _cookies:
            cookies['_cookie_%s' % name] = _cookies[name]
        return cookies
    
    @property
    def request_data(self):
        form_data = {name: self.get_argument(name) for name in self.request.arguments}
        body_data = self._body_data
        req_cookies = copy.deepcopy(self._cache_cookies)
        req_cookies.update(self._cookies)
        request_data = dict(**body_data, **form_data, **req_cookies)
        return request_data

    def get_perfect_request_data(self):
        """
        解析和处理request的参数
        """
        return self.request_data

    async def get(self):
        """
        重写get方法
        """
        kwargs = self.get_perfect_request_data()
        try:
            all_count, data = await self.get_data(**kwargs)
        except HTTP400Error as e:
            return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, e.error_message)
        except HTTP404Error as e:
            return resp.return_error_response(self, resp.HTTP_404_NOT_FOUND, e.error_message)
        return resp.return_success_response(self, data=data, all_count=all_count)


    async def post_data(self, **kwargs):
        return self.model_class.get_object(**kwargs)
    
    async def post(self, **kwargs):
        """
        父类post调用子类的post_data, 实现真正的逻辑
        """
        kwargs = self.get_perfect_request_data()
        try:
            data = await self.post_data(**kwargs)
        except HTTP400Error as e:
            return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, e.error_message)
        except HTTPDetailError as e:
            return resp.response(self, e.error_detail)
        
        return resp.return_success_response(self, data)

    async def put_data(self, **kwargs):
        return self.model_class.get_object(**kwargs)

    async def put(self, **kwargs):
        kwargs = self.get_perfect_request_data()
        # 在数据处理之前可以嵌入django form表单的参数校验
        try:
            data = await self.put_data(**kwargs)
        except HTTP400Error as e:
            return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, e.error_message)
        except HTTPDetailError as e:
            return resp.response(self, e.error_detail)
        
        return resp.return_success_response(self, data)

    async def delete_data(self, **kwargs):
        return self.model_class.get_object(**kwargs)

    async def delete(self, **kwargs):
        kwargs = self.get_perfect_request_data()
        try:
            data = await self.delete_data(**kwargs)
        except HTTP400Error as e:
            return resp.return_error_response(self, resp.HTTP_400_BAD_REQUEST, e.error_message)
        except HTTPDetailError as e:
            return resp.response(self, e.error_detail)
        
        return resp.return_success_response(self, data)
        