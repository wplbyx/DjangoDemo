from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from common.model import BaseModel
from common.manager import get_manager
from common.queryset import BaseCustomQuerySet
from common.uid_builder import new_id

from .article import Article


class CommentQuerySet(BaseCustomQuerySet):
    """ 拓展 QuerySet 类，使得可以自定义方法链式查询 """


class Comment(BaseModel):
    """"""
    uid = models.BigIntegerField(verbose_name="评论ID", primary_key=True, default=new_id, editable=False)

    objects = get_manager(CommentQuerySet)  # 使用拓展查询管理器

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name


#####################################################################
#                           注册事件监听函数                         #
#  post_save(sender, instance, created, raw, using, update_fields)  #
#####################################################################

@receiver(post_save, sender=Article)
def update_courseware_deleted(sender, instance, created, **kwargs):
    """ 监听 Article 文章删除事件，文章相关的评论需要同步删除 """
    if created or not instance.deleted:
        return
    Comment.objects.filter(ware__uid=instance.uid, deleted=False).update(deleted=True)


