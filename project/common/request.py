#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
"""
from rest_framework.generics import GenericAPIView
from common.view_mixins import CreateViewMixin, RetrieveViewMixin, UpdateViewMixin, DestroyViewMixin


class CustomAPIView(GenericAPIView):
    """
    拓展 GenericAPIView 对象：
        添加一个 query_validate_class 属性，用于过滤查询参数类型
    """
    query_validate_class = None  # 拓展查询验证器

    def get_query_validator(self, data):
        return self.query_validate_class(data)


class CreateView(CreateViewMixin, CustomAPIView):
    def post(self, request, *args, **kwargs):
        """ 通用创建功能 """
        return self.create(request, *args, **kwargs)


class RetrieveView(RetrieveViewMixin, CustomAPIView):
    def get(self, request, *args, **kwargs):
        """ 通用查询功能(单个) """
        return self.retrieve(request, *args, **kwargs)


class UpdateView(UpdateViewMixin, CustomAPIView):
    def put(self, request, *args, **kwargs):
        """ 通用更新功能 """
        return self.update(request, *args, **kwargs)


class DeleteView(DestroyViewMixin, CustomAPIView):
    def delete(self, request, *args, **kwargs):
        """ 通用删除功能 """
        return self.destroy(request, *args, **kwargs)


# 拓展

class CRView(CreateViewMixin,
             RetrieveViewMixin,
             CustomAPIView):
    """ 具有 CRUD 功能的视图 """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CRUDView(CreateViewMixin,
               RetrieveViewMixin,
               UpdateViewMixin,
               DestroyViewMixin,
               CustomAPIView):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

