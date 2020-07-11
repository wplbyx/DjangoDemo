#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
数据库模型 字段选择
"""

# 草稿， 定稿
STATUS_DRAFT, STATUS_FINAL = "draft", "final"
COURSE_STATUS = ((STATUS_DRAFT, "草稿"), (STATUS_FINAL, "定稿"))

# 模板， 实物
CATEGORY_TEMPLATE, CATEGORY_INSTANCE = "template", "instance"
COURSE_CATEGORY = ((CATEGORY_TEMPLATE, "模板"), (CATEGORY_INSTANCE, "实物"))
