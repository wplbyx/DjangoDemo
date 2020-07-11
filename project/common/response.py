#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
使用 rest_framework.response.Response 对象方便做api接口调试

"""
from django.shortcuts import render as django_render
from rest_framework.response import Response


def success(data="", status=200):
    """ 返回成功 json 数据 """
    return Response({"data": data}, status=status)


def failure(message="", status=400):
    """ 返回失败 json 数据 """
    return Response({"error": message}, status=status)


def render(request, template_name, context=None):
    """ 返回指定渲染页面 """
    return django_render(request, template_name, context)
