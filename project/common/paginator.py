#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
"""
from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    """ 全局配置：
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'common.paginator.CustomPagination',
        'PAGE_SIZE': 10  # 默认每页条数
    }

    """

    max_limit = 100  # 每页最大条数
    limit_query_param = 'size'  # 每页条数 默认 limit
    offset_query_param = 'page'  # 当前页码 默认 offset

    def get_paginated_response(self, data):
        """ 覆盖默认分页返回结果，这里仅仅返回dict字典结构 """
        return OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('prev', self.get_previous_link()),
            ('results', data)
        ])

