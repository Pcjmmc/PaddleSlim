# -*- coding:utf8 -*-

import base64
import hashlib
import hmac
import json
import logging
import os
import time

from https.send_requests import send_http_request

logger = logging.getLogger('ce')
class empty:
    """
    This class is used to represent no data being provided for a given input
    or output value.

    It is required because `None` may be a valid input or output value.
    """
    pass


class BaseRpc(object):
    method = 'get'
    gateway = ''
    api = ''
    params_keys = ()    # 例如：({'key': 'xxxx', 'type': str},)    HTTP Content-Type为：application/x-www-form-urlencoded
    json_keys = ()    # 例如：({'key': 'xxxx', 'type': str},)      HTTP Content-Type为：application/json
    response_keys = ()  # 例如：({'status': 200, 'type': int},)
    params = {}
    headers = {}
    auth = None
    proxy = None
    need_data = False

    def __init__(self, params=empty, headers=empty):
        self.params = params if (params is not empty) else {}
        self.headers = headers if (headers is not empty) else {}
        self._response = None
        self._response_text = None
        self._called_is_valid = False
        self._errors = None
        self._status = None
        self._params = {}
        self._json_data = {}

    async def is_valid(self):
        self._called_is_valid = True
        self.check_params()
        await self.call()
        if self._errors:
            return False
        return True


    def is_response_success(self):
        """
        判断返回结果是否成功 （判断返回结果中的状态码是否是成功状态，如：200）
        :return:
        """
        assert hasattr(self, '_called_is_valid'), (
            'You must call `.is_valid()` before call `.is_response_success()`'
        )
        return str(self.response_json.get('status')) == str(200)

    @property
    def errors(self):
        assert hasattr(self, '_called_is_valid'), (
            'You must call `.is_valid()` before call attribute `errors`'
        )
        return getattr(self, '_errors', None)

    @property
    def response(self):
        assert hasattr(self, '_called_is_valid'), (
            'You must call `.is_valid()` before call attribute `response`'
        )
        return self._response

    @property
    def response_json(self):
        assert hasattr(self, '_called_is_valid'), (
            'You must call `.is_valid()` before call attribute `response_json`'
        )
        try:
            return json.loads(self._response_text)
        except:
            return self._response_text

    def get_cleaned_data(self, params_keys):
        cleaned_data = {}
        for item in params_keys:
            item_key = item['key']
            item_type = item['type']
            required = item.get('required', True)
            if item_key not in self.params and required:
                self._errors = 'Params `%s` is required.' % item_key
                break
            if item_key not in self.params:
                continue
            if not isinstance(self.params[item_key], item_type):
                has_errors = True
                if callable(item_type):
                    try:
                        self.params[item_key] = item_type(self.params[item_key])
                        has_errors = False
                    except:
                        pass
                if has_errors:
                    self._errors = 'Params `%s` data type must be [%s].' % (item_key, item_type.__name__)
                    break
            cleaned_data[item_key] = self.params[item_key]
        return cleaned_data

    def check_params(self):
        self._params = self.get_cleaned_data(self.params_keys)
        self._json_data = self.get_cleaned_data(self.json_keys)

    @property
    def response_cookies(self):
        cookies = {}
        if not self.response:
            return cookies

        for key, value in self.response.cookies.items():
            cookies[key] = value.value
        return cookies

    async def call(self):
        call_url = os.path.join(self.gateway, self.api)
        print('call url is', call_url)
        start_time = time.time()
        try:
            response, response_text = await send_http_request(access_url=call_url,
                                                              access_params=self._params,
                                                              method=self.method,
                                                              json=self._json_data,
                                                              auth=self.auth,
                                                              proxy=self.proxy,
                                                              **{'headers': self.headers})
        except Exception as e:
            self._errors = e.args
            lost_time = time.time() - start_time
            self.write_log(call_url, error_message=self._errors, lost_time=lost_time)
            return

        lost_time = time.time() - start_time
        self._response = response
        self._status = response.status
        self._response_text = response_text
    def write_log(self, url, response=None, response_text=None, error_message=None, lost_time=None): 
        pass
