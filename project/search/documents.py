#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a description of this module:

-------------------------------------------
|     ElasticSearch      |      MySQL     |
-------------------------------------------
|         Index          |    Database    |
|         Type           |      Table     |
|        Document        |      Row       |
|        Column          |      Field     |
|        schema          |     mapping    |
-------------------------------------------

"""

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from posts.models.article import Article
from posts.models.comment import Comment


@registry.register_document
class ArticleDocument(Document):
    """ 建立索引类 """

    class Index:
        name = 'blog'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Article
        fields = ['uid', 'title']


@registry.register_document
class CommentDocument(Document):
    """"""

    class Index:
        name = "blog"

    class Django:
        model = Comment
        fields = ["index", "status"]
