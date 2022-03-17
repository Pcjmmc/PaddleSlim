"""
Descriptive HTTP status codes, for code readability.

See RFC 2616 - https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
And RFC 6585 - https://tools.ietf.org/html/rfc6585
And RFC 4918 - https://tools.ietf.org/html/rfc4918
"""
from __future__ import unicode_literals


def is_informational(code):
    """
    信息性的返回码
    """
    return 100 <= code <= 199


def is_success(code):
    """
    成功返回码
    """
    return 200 <= code <= 299


def is_redirect(code):
    """
    跳转返回码
    """
    return 300 <= code <= 399


def is_client_error(code):
    """
    客户端错误返回码
    """
    return 400 <= code <= 499


def is_server_error(code):
    """
    服务段错误返回码
    """
    return 500 <= code <= 599

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_500_INTERNAL_SERVER_ERROR = 500

