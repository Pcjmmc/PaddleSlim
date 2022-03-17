# encoding: utf-8
"""
generate md5
"""
import hashlib


def get_md5(content):
    """
    获取字符串的md5
    """
    m = hashlib.md5()
    m.update(content.encode('utf-8'))
    return m.hexdigest()
