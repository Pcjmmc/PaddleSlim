"""
封装sqlalchmy的column
"""
from sqlalchemy import Column as SaColumn


class Column(SaColumn):
    """
    重写sqlalchmy的column，将为空的字段自动过滤掉
    """
    def __init__(self, *args, **kwargs):
        nullable = False
        if 'nullable' in kwargs:
            nullable = kwargs.pop('nullable')

        super().__init__(*args, nullable=nullable, **kwargs)
