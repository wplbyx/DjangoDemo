#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:

参考链接：
    https://www.cnblogs.com/lddragon1/p/12113437.html

"""
from traceback import format_exc
from common.response import success, failure
from common.logger import CustomLogger

logger = CustomLogger("request")  # 使用 request logger 实例记录日志


class CreateViewMixin:
    """ 通用创建 Mixin 对象
    子类需要指定 queryset, serializer_class 两个类成员属性
    """

    def create(self, request, *args, **kwargs):
        """ 创建就是传递一堆数据表单验证 """
        request_data = request.data
        many = isinstance(request_data, list)

        try:
            serializer = self.get_serializer(data=request_data, many=many)
            if not serializer.is_valid():
                return failure(serializer.errors)

            # 批量创建有2种方式: 1. 当前方式， 2. 类似于批量修改的方式，使用辅助类 ListSerializer
            ModelClass = serializer.Meta.model  # 获取当前Model类对象
            validated_data = dict(serializer.validated_data)
            ModelClass.objects.create(**validated_data)
            return success("创建成功", status=201)
        except Exception as e:
            logger.error(format_exc())  # format_exc 用于获取异常栈信息，随后记录完整日志
            return failure("系统错误，创建失败", 500)


class UpdateViewMixin:
    """ 通用更新 Mixin 对象 """

    def update(self, request, *args, **kwargs):
        """ 更新数据 """
        ids = []
        request_data = request.data
        for idx, obj in enumerate(request_data):
            obj_id = obj.get('uid', None)
            if not obj_id:
                continue
            ids.append(obj_id)

        update_instance = self.get_queryset().useful().filter(uid__in=ids).all()
        if len(ids) != len(update_instance):
            return failure("没有找到对应的数据")

        serializer = self.get_serializer(instance=update_instance, data=request.data, many=True, partial=True)
        if not serializer.is_valid():
            return failure(serializer.errors)

        serializer.save()
        return success("更新成功")


class DestroyViewMixin:
    """ 通用删除 Mixin 对象，
    需要联级修改状态，使用消息监听的方式
    """

    def destroy(self, request, *args, **kwargs):
        """ 单个删除 """
        try:
            delete_ids = request.data.get("ids", [])
            self.get_queryset().useful().filter(uid__in=delete_ids).update(deleted=True)
            return success("删除成功")
        except Exception as e:
            logger.error(format_exc())  # format_exc 用于获取异常栈信息，随后记录完整日志
            return failure("删除失败")


class RetrieveViewMixin:
    """ 通用查询 Mixin 对象

    一种过滤查询思路：
        查询条件的key 当做拓展QuerySet对象里的函数，
        有一个查询条件就单独写一个对应的方法过滤，然后改函数就返回一个过滤之后的查询集(QuerySet) 方便链式调用
        例子：
            query_dict: {name: "jack", age_max: "18"}  # 默认补充一个 many 字段

            # 其中 query_name(), query_age_max() 都是 QuerySet 自定义拓展方法
            SomeModel.objects.useful().query_name().query_age_max()



    问题：如果跨表查询也行吗？... 如何处理跨表问题？...

    问题：如何处理权限问题？ 对象级别的权限，中间件拦截？？？ 利用 django-guardian 类似的思路


    """

    def retrieve(self, request, *args, **kwargs):
        """ include, exclude
        1. 处理查询集合
        2. 需要分页
        get_query_validator
        """
        page_number_key = self.paginator.offset_query_param  # 获取分页字符串
        page = request.query_params.get(page_number_key, None)  # 用于判断是否分页
        first = request.query_params.get('first', None)         # 指定是否查询第一条数据

        # 处理查询
        try:
            validator = self.get_query_validator(request.query_params.dict())
            if not validator.is_valid():
                return failure(validator.errors.as_json(), 400)

            ModelClass = self.serializer_class.Meta.model  # 获取当前Model类对象
            queryset = ModelClass.queryset_builder(validator.cleaned_data)  # 构建查询结果集 QuerySet
        except Exception as e:
            logger.error(format_exc())  # format_exc 用于获取异常栈信息，随后记录完整日志
            return failure("处理查询条件失败", 400)

        if first:  # 查询单条记录
            serializer = self.get_serializer(queryset.first())
        elif page:  # 分页记录
            page_datas = self.paginate_queryset(queryset)  # return: None or list
            serializer = self.get_serializer(page_datas, many=True)
            paginated_data = self.get_paginated_response(serializer.data)  # 这里需要使用自定义的分页器
            return success(paginated_data)
        elif queryset:  # 默认查询全部记录
            serializer = self.get_serializer(queryset, many=True)
        else:  # 没有查询到数据返回空列表
            return success([])

        return success(serializer.data)

