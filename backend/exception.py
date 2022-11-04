# -*- coding:utf8 -*-
"""
异常模块的定义
"""
class HTTP400Error(Exception):
    """
    An exception that will turn into an HTTP error response.
    """
    _error_message = 'HTTP error: Bad request'

    def __init__(self, error_message=None):
        self.error_message = error_message or self._error_message

    def __str__(self):
        return self.error_message

class HTTP401Error(Exception):
    """
    An exception that will turn into an HTTP error response.
    """
    _error_message = 'Authenticate error: Permission verification failed!'

    def __init__(self, error_message=None):
        self.error_message = error_message or self._error_message

    def __str__(self):
        return self.error_message

class HTTPDetailError(Exception):
    """
    An exception that will turn into an HTTP error response with detail.
    """
    _error_message = 'HTTP error: Bad request'

    def __init__(self, error_message=None, error_detail=None):
        self.error_message = error_message or self._error_message
        self.error_detail = error_detail

    def __str__(self):
        return self.error_message

class HTTP404Error(Exception):
    """
    An exception that will turn into an HTTP error response.
    """
    _error_message = 'HTTP error: Message Not Found'

    def __init__(self, error_message=None):
        self.error_message = error_message or self._error_message

    def __str__(self):
        return self.error_message