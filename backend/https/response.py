# # -*- coding:utf8 -*-
"""
返回结果的处理
"""
from https import status as _status

import copy

HTTP_200_OK = {
    'code': 200,
    'message': 'success',
    'data': [],
}
HTTP_400_BAD_REQUEST = {
    'code': 400,
    'message': 'Bad Request!'
}

HTTP_401_BAD_REQUEST = {
    'code': 401,
    'message': 'Authenticate error: Permission verification failed!'
}

HTTP_404_NOT_FOUND = {
    'code': 404,
    'message': 'Message Not Found!'
}

HTTP_405_METHOD_NOT_ALLOWED = {
    'code': 405,
    'message': 'Method Not Allowed!'
}
HTTP_500_INTERNAL_SERVER_ERROR = {
    'code': 500,
    'message': 'Server Error Or Unlawful Request!'
}

HTTP_4001_INTERNAL_SERVER_ERROR = {
    'code': 4001,
    'message': 'Redirect To New Url!'
}

STATUS_LIST = (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_4001_INTERNAL_SERVER_ERROR, HTTP_401_BAD_REQUEST
)


def response(tornado_request_handler, response_content, status=200):
    """
    :param response_content: return content
    :param status: return code
    """
    tornado_request_handler.set_status(status_code=status)
    tornado_request_handler.write(response_content)


def return_error_response(tornado_request_handler, http_status, error_message=None):
    """
    :param tornado_request_handler: tornado.web.requestHandler
    :param http_status:
    :param error_message:
    :return:
    """
    if http_status not in STATUS_LIST:
        return response(tornado_request_handler, HTTP_500_INTERNAL_SERVER_ERROR, status=_status.HTTP_200_OK)

    response_error = copy.copy(http_status)
    if error_message:
        response_error['message'] = error_message
    return response(tornado_request_handler, response_error, status=_status.HTTP_200_OK)

def return_redirect_response(tornado_request_handler, http_status, new_url=None):
    """
    :param tornado_request_handler: tornado.web.requestHandler
    :param http_status:
    :param error_message:
    :return:
    """
    if http_status not in STATUS_LIST:
        return response(tornado_request_handler, HTTP_500_INTERNAL_SERVER_ERROR, status=_status.HTTP_200_OK)

    response_error = copy.copy(http_status)
    if new_url:
        response_error['message'] = new_url
    return response(tornado_request_handler, response_error, status=_status.HTTP_200_OK)

def return_success_response(tornado_request_handler, data=None, **kwargs):
    """
    :param tornado_request_handler: tornado.web.requestHandler
    :param data:
    :param kwargs:
    :return:
    """
    response_success = copy.copy(HTTP_200_OK)
    response_success['data'] = data
    response_success.update(**kwargs)
    return response(tornado_request_handler, response_success, status=_status.HTTP_200_OK)
