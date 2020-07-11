#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:
ModelSerialize 拓展辅助类, 实现批量修改和批量创建
"""

from rest_framework.serializers import ListSerializer


class CustomListSerializer(ListSerializer):
    """
    拓展 DRF ListSerializer, 实现自定义批量更新操作
    """

    def create(self, validated_data):
        """ 批量创建 """
        try:
            ModelClass = self.child.Meta.model  # self.child --> ModelSerializer
            batch = [ModelClass(**attrs) for attrs in validated_data]
            ModelClass.objects.bulk_create(batch)
            return True
        except:
            return False

    def update(self, instance_list, validated_data_list):
        """ 批量更新 """
        try:
            for idx, attrs in enumerate(validated_data_list):
                self.child.update(instance_list[idx], attrs)
            return True
        except:
            return False
