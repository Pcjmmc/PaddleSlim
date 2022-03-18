# -*- coding:utf8 -*-
"""
项目数据库路由
"""
class ModelRouter(object):
    """
    控制项目中模型的所有数据库操作的路由
    """
    def db_for_operation(self, model, **hints):
        """
        找到模型相应的db名
        """
        if hasattr(model, 'Meta'):
            return getattr(model.Meta, 'app_label', 'default')
        return 'paddle_quality'
