# !/usr/bin/env python3
# -*- coding:utf8 -*-
"""
封装mysql的基本操作，实现连接和增删改查等操作
"""
import asyncio
import json
import time
import traceback
import urllib.parse

import sqlalchemy as sa
from aiomysql.sa import create_engine as aiomysql_create_engine
from ce_web.router import ModelRouter
from ce_web.settings.common import STORAGE
from sqlalchemy import column, desc, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql import and_, not_, or_
from sqlalchemy.sql.schema import ColumnDefault


class BaseEngine(object):
    """
    创建所有数据的连接engin
    """
    aio_db_engines = {}
    echo = False

    def __init__(self, env='DEV'):
        # 开发环境
        if env == 'DEV':
            self.echo = True

    async def aio_create_engine(self):
        """
        create db engin
        """
        database = STORAGE["mysql"]
        _db_engines = {}
        for db_key, db_config in database.items():
            db_engine = await aiomysql_create_engine(
                host=db_config['host'], port=db_config['port'],
                user=db_config['user'], password=db_config['password'],
                db=db_config['db_name'], autocommit=True
            )
            _db_engines[db_key] = db_engine
        self.aio_db_engines = _db_engines

    @property
    async def aio_engines(self):
        """
        get db engin
        """
        if not self.aio_db_engines:
            await self.aio_create_engine()
        return self.aio_db_engines


# model to dict
@property
def to_dict(self):
    """
    turn attr to dict
    """
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


# 创建基类对象
Base = declarative_base()
Base.to_dict = to_dict
BaseModel = Base

loop = asyncio.get_event_loop()
db_engines = loop.run_until_complete(BaseEngine().aio_engines)


class BaseModelMixin(object):
    """
    封装基类，负责实现数据库的基本操作
    """
    filter_compares = {'in': '.in_()',
                       'lt': '<',
                       'lte': '<=',
                       'gt': '>',
                       'gte': '>=',
                       'ne': '!=',
                       'contains': '.like()'}

    @classmethod
    def model_to_dict(cls, instance):
        """
        将模型转换成dict
        """
        return {column: value for column, value in instance.items()}

    @classmethod
    def get_db_engine(cls):
        """
        获取db engines
        """
        db_key = ModelRouter().db_for_operation(cls)
        try:
            engine = db_engines[db_key]
        except AttributeError:
            engine = db_engines[db_key]
        return engine

    @classmethod
    def get_model(cls, **kwargs):
        """
        获取模型映射的表名
        """
        if hasattr(cls, '__tablename__'):
            return cls

        # 分表
        if not (getattr(cls, '__abstract__', False) and hasattr(cls, '_base_tablename')):
            raise AttributeError('Ths class [%s] has not attribute "__abstract__/_base_tablename"' % cls.__name__)
        else:
            if not hasattr(cls, 'Meta'):
                raise AttributeError('Ths class [%s] has not attribute "Meta"' % cls.__name__)
            if not hasattr(cls.Meta, 'match_table_field'):
                raise AttributeError('Ths class [%s] has not attribute "Meta.match_table_field"' % cls.__name__)
            if not hasattr(cls.Meta, 'match_table_func'):
                raise AttributeError('Ths class [%s] has not attribute "Meta.match_table_func"' % cls.__name__)

            model_id = cls.Meta.match_table_func(kwargs[cls.Meta.match_table_field])
            class_name = '%s_%s' % (cls.__name__, model_id)
            table_name = '%s_%s' % (cls._base_tablename, model_id)

            class_model = type(class_name, (cls,), {'__tablename__': table_name})
            return class_model

    @classmethod
    def orm_fields_info(cls):
        """
        解析orm定义，将定义转换成dict
        """
        fields_info = {}

        for field, orm_instance in cls.__dict__.items():
            if field.startswith('__'):
                continue
            if isinstance(orm_instance, InstrumentedAttribute):
                prop = orm_instance.prop
                if isinstance(prop, ColumnProperty):
                    default = prop.columns[0].default
                    if isinstance(default, ColumnDefault):
                        default = default.arg
                    fields_info[field] = {'type': prop.columns[0].type,
                                          'default': default,
                                          'nullable': prop.columns[0].nullable}
        return fields_info

    @classmethod
    def get_valid_kwargs(cls, **kwargs):
        """
        解析参数，获取有效参数
        """
        _kwargs = {}
        for key, value in kwargs.items():
            if key.startswith('__') or key.startswith('_'):
                continue
            if key in cls.__dict__:
                _kwargs[key] = value
            key_split = key.split('__')
            if len(key_split) != 2:
                continue
            if key_split[1] in cls.filter_compares:
                _kwargs[key] = value
        return _kwargs

    @classmethod
    def make_perfect_init_data(cls, **kwargs):
        """
        处理初始化的参数，没有赋值的采用默认值
        """
        if 'created' in cls.__dict__:
            kwargs['created'] = kwargs.get('created') or int(time.time())
        if 'updated' in cls.__dict__:
            kwargs['updated'] = int(time.time())

        cls.object_to_json(kwargs)

        for field, field_info in cls.orm_fields_info().items():
            if field not in kwargs and field_info['default'] is not None:
                if callable(field_info['default']):
                    # callable function不带参数，但是如果不带参数调用会报如下错误，目前不能确定是哪里的BUG。
                    # 报错信息：TypeError: <lambda>() missing 1 required positional argument: 'ctx'，
                    # 相同错误可参考：https://github.com/thomaxxl/safrs/issues/32
                    kwargs[field] = field_info['default'](None)
                else:
                    kwargs[field] = field_info['default']
        return kwargs

    @classmethod
    def get_filter_eval_str(cls, column, value):
        """
        解析和拼装查询语句
        """
        if '__' in column:
            _column, compare = column.split('__')
            if compare == 'in':
                eval_str = 'queryset.where(cls.%s.in_(kwargs["%s"]))' % (_column, column)
            elif compare == 'contains':
                eval_str = 'queryset.where(cls.%s.like("%s"))' % (_column, '%%%s%%' % value)
            else:
                eval_str = 'queryset.where(cls.%s %s kwargs["%s"])' % (_column,
                                                                       cls.filter_compares[compare],
                                                                       column)
        else:
            eval_str = 'queryset.where(cls.%s == kwargs["%s"])' % (column, column)
        return eval_str

    @classmethod
    def get_query_filter(cls, queryset, **kwargs):
        """
        处理请求参数，拼装查询语句
        """
        for column, value in kwargs.items():
            eval_str = cls.get_filter_eval_str(column, value)

            queryset = eval(eval_str)
        return queryset

    @classmethod
    def make_query_for_db(cls, **kwargs):
        """
        获取db engine及参数

        :param action: 动作（如：查询（filter）、插入数据（insert）、更新数据（update）等）
        :param kwargs: 参数
        :return:
        """
        engine = cls.get_db_engine()
        _kwargs = cls.get_valid_kwargs(**kwargs)
        model_class = cls.get_model(**kwargs)
        return engine, _kwargs, model_class

    @classmethod
    def make_perfect_update_data(cls, **kwargs):
        """
        处理update参数
        """
        cls.object_to_json(kwargs)
        return kwargs

    @classmethod
    def json_to_object(cls, validated_data):
        """
        turn json to object
        """
        if hasattr(cls, 'Meta') and hasattr(cls.Meta, 'json_fields'):
            for field in cls.Meta.json_fields:
                try:
                    validated_data[field] = json.loads(validated_data[field])
                except:
                    pass

    @classmethod
    def object_to_json(cls, validated_data):
        """
        turn db object to json
        """
        if hasattr(cls, 'Meta') and hasattr(cls.Meta, 'json_fields'):
            for field in cls.Meta.json_fields:
                if field in validated_data:
                    validated_data[field] = json.dumps(validated_data[field])


    @classmethod
    def get_query_regroup(cls, queryset, order_by=None, group_by=None):
        """
        queryset添加order by、group by等重新组合条件
        :param queryset:
        :param order_by:
        :param group_by:
        :return:
        """
        if group_by:
            if not isinstance(group_by, (tuple, list)):
                group_by = [group_by]
            for column in group_by:
                eval_str = 'queryset.group_by(cls.%s)' % column
                queryset = eval(eval_str)
        if order_by:
            if not isinstance(order_by, (tuple, list)):
                order_by = [order_by]
            for column in order_by:
                if column.startswith('-'):
                    eval_str = 'queryset.order_by(desc(cls.%s))' % column[1:]
                else:
                    eval_str = 'queryset.order_by(cls.%s)' % column
                queryset = eval(eval_str)
        return queryset

    @classmethod
    async def aio_insert(cls, validated_data=None):
        """
        插入数据
        :param validated_data: 更改的数据
        :return: row_count, last_rowid  (被修改的行数，最后更新的行的行ID)
        """
        engine, _, model_class = cls.make_query_for_db()
        validated_data_list = []
        if isinstance(validated_data, (list, tuple)):
            for value in validated_data:
                _value = cls.get_valid_kwargs(**value)
                _value = cls.make_perfect_init_data(**_value)
                validated_data_list.append(_value)
        elif isinstance(validated_data, dict):
            _value = cls.get_valid_kwargs(**validated_data)
            _value = cls.make_perfect_init_data(**_value)
            validated_data_list.append(_value)
        else:
            raise TypeError('validate_data type must be [tuple | list | dict]')
        queryset = sa.insert(model_class, validated_data_list)
        row_count, last_rowid = await cls.aio_execute(engine, queryset, need_last_rowid=True)
        return row_count, last_rowid

    @classmethod
    async def aio_get_object(cls, order_by=None, group_by=None, **kwargs):
        """
        条件查询
        条件规则写法：in: param__in  (param为要过滤的column) 等同于：in list
                    lt: param__lt      等同于：小于
                    lte: param__lte    等同于：小于等于
                    gt: param__gt      等同于：大于
                    gte: param__gte    等同于：大于等于
                    ne: param__ne      等同于：不等于
                    contains: param__contains  等同于：模糊匹配如： like '%aaa%'
        :param order_by:
        :param group_by:
        :param kwargs:
        :return: instance (类型为：aiomysql.sa.result.RowProxy类对象)
        """
        engine, _kwargs, model_class = cls.make_query_for_db(**kwargs)

        queryset = sa.select([model_class])
        queryset = cls.get_query_filter(queryset, **_kwargs)
        queryset = cls.get_query_regroup(queryset, order_by, group_by)

        async with engine.acquire() as conn:
            await conn._connection.ping()
            trans = await conn.begin()
            try:
                result = await conn.execute(queryset)
                await trans.commit()
                return await result.fetchone()
            except Exception as e:
                print("except is", e)
                traceback.format_exc()
                await trans.rollback()
                return None

    @classmethod
    async def aio_filter_objects(cls, page_index=1, limit=20, need_all=False, order_by=None, group_by=None, **kwargs):
        """
        条件查询
        条件规则写法：in: param__in  (param为要过滤的column) 等同于：in list
                    lt: param__lt      等同于：小于
                    lte: param__lte    等同于：小于等于
                    gt: param__gt      等同于：大于
                    gte: param__gte    等同于：大于等于
                    ne: param__ne      等同于：不等于
                    contains: param__contains  等同于：模糊匹配如： like '%aaa%'
        :param page_index: 分页下标值
        :param limit:
        :param need_all:
        :param order_by:
        :param group_by:
        :param kwargs:
        :return: instance list (每个元素为：aiomysql.sa.result.RowProxy类对象)
        """
        engine, _kwargs, model_class = cls.make_query_for_db(**kwargs)
        if group_by:
            # group by只能查询分组的字段
            if not isinstance(group_by, (tuple, list)):
                group_by = [group_by]
            columns = [column(col) for col in group_by]
            queryset = sa.select(columns=columns, from_obj=model_class)
        else:
            # 相当于select *
            queryset = sa.select([model_class])
        queryset = cls.get_query_filter(queryset, **_kwargs)
        queryset = cls.get_query_regroup(queryset, order_by, group_by)

        if not need_all:
            offset = (int(page_index) - 1) * int(limit)
            queryset = queryset.offset(offset).limit(int(limit))
        async with engine.acquire() as conn:
            await conn._connection.ping()
            trans = await conn.begin()
            try:
                result = await conn.execute(queryset)
                await trans.commit()
                instances = await result.fetchall()
                return instances
            except Exception as e:
                print("except is", e)
                await trans.rollback()
                return []

    @classmethod
    async def aio_filter_details(cls, page_index=1, limit=20, need_all=False, order_by=None, group_by=None, **kwargs):
        """
        条件查询
        :param page_index:
        :param limit:
        :param need_all: 
        :param order_by:
        :param group_by:
        :param kwargs:
        :return: list (元素为：dict)
        """
        instances = await cls.aio_filter_objects(page_index=page_index, limit=limit, need_all=need_all, order_by=order_by, group_by=group_by, **kwargs)
        if not instances:
            return instances

        details = []
        for ins in instances:
            detail = cls.model_to_dict(ins)
            cls.json_to_object(detail)
            details.append(detail)
        return details

    @classmethod
    async def aio_filter_count(cls, order_by=None, group_by=None, **kwargs):
        """
        条件查询 - 查询总数
        :param kwargs:
        :return: 符合条件的总数
        """
        engine, _kwargs, model_class = cls.make_query_for_db(**kwargs)

        queryset = sa.select([func.count(model_class.id)])
        queryset = cls.get_query_filter(queryset, **_kwargs)
        queryset = cls.get_query_regroup(queryset, order_by, group_by)

        async with engine.acquire() as conn:
            await conn._connection.ping()
            result = await conn.execute(queryset)
            count_proxy = await result.fetchone()

        count = None
        for column, value in count_proxy.items():
            count = value
            break
        return count

    @classmethod
    async def aio_filter_details_with_total_count(cls, page_index=1, limit=20, need_all=False, **kwargs):
        """
        条件查询 - 分页查询，并返回总数
        :param kwargs:
        :return: 符合条件的总数和数据
        """
        job_tasks = [
            cls.aio_filter_count(**kwargs),
            cls.aio_filter_details(page_index=page_index, limit=limit, need_all=need_all, **kwargs)
        ]
        result = await asyncio.gather(*job_tasks)
        return result[0], result[1]

    @classmethod
    async def aio_update(cls, validated_data=None, params_data=None):
        """
        更新数据
        :param validated_data: 更改的数据
        :param params_data: 过滤条件
        :return: row count
        """
        engine, _params_data, model_class = cls.make_query_for_db(**params_data)
        validated_data = cls.make_perfect_update_data(**validated_data)
        # 如果有updated则强制更新
        if 'updated' in cls.__dict__:
            validated_data['updated'] = int(time.time())
        queryset = sa.update(model_class)
        queryset = cls.get_query_filter(queryset, **_params_data)
        queryset = queryset.values(**validated_data)
        row_count, _ = await cls.aio_execute(engine, queryset)
        return row_count

    @classmethod
    async def aio_delete(cls, params_data=None):
        """
        删除数据
        :param params_data: 参数
        :return:
        """
        engine, _params_data, model_class = cls.make_query_for_db(**params_data)

        queryset = sa.delete(model_class)
        queryset = cls.get_query_filter(queryset, **_params_data)

        row_count, _ = await cls.aio_execute(engine, queryset)
        return row_count

    @classmethod
    async def aio_execute(cls, engine, queryset, need_last_rowid=False):
        """
        aiomysql执行SQL语句
        :param engine:
        :param queryset:
        :param need_last_rowid:
        :return: row_count, last_rowid (被修改的行数, 最后一行ID)
        """
        row_count = 0
        last_rowid = 0     # 当row_count不为0，last_rowid才有效
        async with engine.acquire() as conn:
            await conn._connection.ping()
            trans = await conn.begin()
            try:
                result = await conn.execute(queryset)
                row_count = result.rowcount
                last_rowid = result.lastrowid
            except Exception as e:
                print(e)
                traceback.format_exc()
                await trans.rollback()
            else:
                await trans.commit()

        if need_last_rowid:
            return row_count, last_rowid
        return row_count, None
