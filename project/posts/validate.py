#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:

使用 Django Form 来实现查询字段类型验证功能

"""

from django import forms


class ArticleQueryValidate(forms.Form):
    """ 查询字段验证
    使用方式：

        query_dict = request.query_params.dict()  # QueryDict 转 dict
        validator = CoursewareQueryValidate(query_dict)
        if not validator.is_valid()
            return failure(validator.errors.as_json())  # 将错误信息以json方式返回

        # 可以继续后面的查询使用了
        data = validator.cleaned_data  # 过滤之后的数据(已经转换好类型了)

    """
    id = forms.IntegerField(required=False)

