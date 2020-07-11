from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from common.model import BaseModel
from common.manager import get_manager
from common.queryset import BaseCustomQuerySet
from common.uid_builder import new_id


class ArticleQuerySet(BaseCustomQuerySet):
    """ 拓展 QuerySet 类，使得可以自定义方法链式查询 """


class Article(BaseModel):
    """"""
    uid = models.BigIntegerField(verbose_name="文章标识", primary_key=True, default=new_id, editable=False)

    objects = get_manager(ArticleQuerySet)  # 使用拓展查询管理器

    class Meta:
        db_table = 'tb_article'
        verbose_name = '博客文章内容'
        verbose_name_plural = verbose_name


#####################################################################
#                           注册事件监听函数                         #
#  post_save(sender, instance, created, raw, using, update_fields)  #
#####################################################################

# @receiver(post_save, sender=Courseware)
# def update_courseware_deleted(sender, instance, created, **kwargs):
#     if created or not instance.deleted:
#         return
#     CourseChapter.objects.filter(ware__uid=instance.uid, deleted=False).update(deleted=True)


