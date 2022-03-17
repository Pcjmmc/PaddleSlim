# -*- coding:utf8 -*-
import aiohttp
from tornado.web import RequestHandler


def sorted_dict_values(adict):
    items = list(adict.items())
    items.sort()
    return [str(x[1]) for x in items]


async def send_http_request(access_url, access_params, method='get', json=None, **kwargs):
    """
    发送http request请求
    """
    if method.upper() not in RequestHandler.SUPPORTED_METHODS:
        raise TypeError("Http request cannot support the [%s] method!" % method)

    _kwargs = {'params': None, 'data': None, 'json': None, 'headers': None, 'auth': None}
    if 'headers' in kwargs:
        _kwargs['headers'] = kwargs['headers']
    
    if 'auth' in kwargs:
        _kwargs['auth'] = kwargs['auth']

    if method.upper() in ('GET', 'HEAD', 'OPTIONS'):
        _kwargs['params'] = access_params
    else:
        if json:
            _kwargs['json'] = json
        else:
            _kwargs['data'] = access_params

    async with aiohttp.ClientSession() as session:
        # 根据方法去获取属性，然后发送请求
        handle = getattr(session, method)
        async with handle(access_url, **_kwargs) as response:
            return response, await response.text()

