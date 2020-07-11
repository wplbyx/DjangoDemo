from django.urls import path
from .search import full_text_search

urlpatterns = [

    path('search/', full_text_search),  # 一个查询接口

]