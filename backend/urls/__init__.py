# -*- coding:utf8 -*-
"""
封装url include模块（tornado没有实现）
"""
import warnings
from importlib import import_module
import os


class RegexURLPattern(object):
    """
    实现单个url的路径和view的映射关系
    """
    def __init__(self, regex, callback, default_kwargs=None, name=None):
        self.regex = regex
        self.callback = callback
        self.default_kwargs = default_kwargs

    @property
    def url(self):
        """
        实现单个url的路径和view的映射关系
        """
        patterns = (self.regex, self.callback, self.default_kwargs)
        return patterns


class RegexURLResolver(object):
    """
    实现多个url的路径和view的映射关系
    """
    def __init__(self, regex, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        self.regex = regex
        self.urlconf_name = urlconf_name
        self.default_kwargs = default_kwargs

    @property
    def url(self):
        """
        实现多个url的路径和view的映射关系
        """
        urlpatterns = [(os.path.join(self.regex, url_pattern.regex), url_pattern.callback, url_pattern.default_kwargs)
                       for url_pattern in self.urlconf_name]
        return urlpatterns


def include(arg, namespace=None, app_name=None):
    """
    实现include的功能
    """
    if app_name and not namespace:
        raise ValueError('Must specify a namespace if specifying app_name.')

    urlconf_module = arg
    if isinstance(urlconf_module, (str, bytes)):
        urlconf_module = import_module(urlconf_module)
    patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
    return patterns


def url(regex, view, kwargs=None, name=None):
    """
    对路径url的view映射关系的封装
    """
    if isinstance(view, (list, tuple)):
        # For include(...) processing.
        return RegexURLResolver(regex, view, kwargs, name)
    elif callable(view):
        return RegexURLPattern(regex, view, kwargs, name)
    else:
        raise TypeError('view must be a callable or a list/tuple in the case of include().')

