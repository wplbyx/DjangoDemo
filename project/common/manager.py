#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
"""

from itertools import chain
from django.db.models.manager import Manager


class BaseCustomManager(Manager):
    """ 自定义通用 Manager，这里编写 Manager 通用方法(表级) """

    def queryset_builder(self, params, extent=None):
        """
        根据 params 构建符合规则的 query_set 对象，
        拓展 Manager 统一实现查询(query) 功能复用，任何地方都可以这样调用：

        queryset = SomeModel.objects.queryset_builder(**kwargs)  # queryset 一个未序列化的查询结果集

        关于拓展方法 query_xxxxx(value, params) 方法的介绍：
            函数名称表示了当前需要查询的字段
            query_{func}(value, params) 是存在于 QuerySet 拓展类的自定义函数，
                value:  当前过滤的参数
                params: 当前查询的所有参数，用于需要更多参数的查询

        ***********************************************************************************

        :param params: 经过验证过滤的查询字段
        :param extent: 需要内部额外补充的字段 默认{}
        :return:
        """
        extends = extent if isinstance(extent, dict) else {}
        queryset_result = self.get_queryset()  # 初始化查询集
        for func, value in chain(params.items(), extends.items()):  # 以此迭代两个字典
            if not value:  # 过滤空查询条件
                continue
            query_func_name = f'query_{func}'  # 指定query_func名称
            if not hasattr(queryset_result, query_func_name):  # 过滤没有定制查询方法的key
                continue

            # 动态叠加链式查询集
            queryset_result = getattr(queryset_result, query_func_name)(value, params)

        # 有的模型没有 deleted 字段，需要过滤 deleted=True 的数据
        try:
            queryset_result = queryset_result.useful()
        except:
            pass

        return queryset_result


def get_manager(queryset, *managers):
    """
    获取基于自定义 QuerySet 所构建的 Manager 对象
    :param queryset: 拓展 QuerySet 对象
    :param managers: 拓展 Manager 对象列表， 高层类(父) --->  低层类(子)
    :return: Manager 对象
    """
    # 如果有额外的拓展Manger对象，就将其混入到 BaseCustomManager 拓展类当中去
    ResultManager = BaseCustomManager
    if managers:
        bases = tuple(manager for manager in managers if issubclass(manager, Manager))
        ResultManager.__bases__ += bases  # 合并继承关系(添加跟多的父类)，针对于不同的 Model.objects 添加不同的拓展方法

    return ResultManager.from_queryset(queryset)()
    # return BaseCustomManager.from_queryset(queryset)()
