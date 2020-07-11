#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
权限管理
"""
# from rest_framework.permissions import BasePermission
#
#
# class CustomObjectPermissions(BasePermission):
#     """ 自定义对象级别权限 django-guardian """
#
#     def has_permission(self, request, view):
#         """"""
#
#     def has_object_permission(self, request, view, obj):
#         """"""
#         queryset = self._queryset(view)
#         model_cls = queryset.model
#         user = request.user


from functools import wraps
from inspect import signature

"""
===========  实验东西  ===========

装饰器对象，需要使用到被装饰函数的参数列表里的对象：
"""


def check_permission_table(func):
    """ 表级别权限检测装饰器 """
    # print('table: ', func.__defaults__, func.__kwdefaults__)
    print('table: ', signature(func))

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("execute: check_permission_table...")
        return func(*args, **kwargs)

    return wrapper


def check_permission_object(some=None):
    """ 对象级别权限验证装饰器 """

    # print('object:', func.__defaults__, func.__kwdefaults__)

    def wrapper(func):
        request = signature(func).parameters.get("request")
        print('object:', request)

        print(signature(func))
        print(signature(func).replace(return_annotation="def"))

        function = signature(func).replace(return_annotation="hello world")

        @wraps(func)
        def inner(*args, **kwargs):
            print("execute: check_permission_object...")
            # sig.replace(return_annotation="wrapper func...")
            return function(*args, **kwargs)

        return inner

    return wrapper


@check_permission_table
@check_permission_object()
def hello(request=1, aa=None, bb=None, cc=None):
    print("hello")


if __name__ == "__main__":
    print(hello(request=0, cc=3))

    pass
