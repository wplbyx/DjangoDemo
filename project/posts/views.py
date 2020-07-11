from common.request import CRUDView
from posts.serializes import ArticleSerialize
from posts.validate import ArticleQueryValidate
from .models.article import Article


class ArticleView(CRUDView):
    """ 文章视图类 """

    queryset = Article.objects.all()
    serializer_class = ArticleSerialize
    query_validate_class = ArticleQueryValidate
