from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    """ 提炼通用字段 """

    created = models.DateTimeField(verbose_name="创建时间", default=datetime.now, null=True, blank=True)
    updated = models.DateTimeField(verbose_name="更新时间", default=datetime.now, null=True, blank=True)
    deleted = models.BooleanField(verbose_name="逻辑删除", default=False)

    class Meta:
        abstract = True
