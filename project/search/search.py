

from rest_framework.decorators import api_view

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch, Match

from common.response import success, failure

client = Elasticsearch()  # 创建客户端


def full_text_search(request):
    """
    # 可行方案
    keywords = request.GET.get("search", "")
    response = client.search(index="course", body={
        "query": {
            "multi_match": {
                "query": keywords,
                "fields": ["description"]
            }
        }
    })
    return success(response)
    """
    # 可行方案
    keywords = request.GET.get("search", "")
    response = client.search(index="blog", body={
        "query": {
            "multi_match": {
                "query": keywords,
                "fields": ["description"]
            }
        }
    })
    return success(response)

    # # 可行方案
    # keywords = request.GET.get("search", "")
    # response = client.search(index="course", body={
    #     "query": {
    #         "multi_match": {
    #             "query": keywords,
    #             "fields": ["description"]
    #         }
    #     }
    # })
    # return success(response)

    # keywords = request.GET.get("search", "")
    # search = Search(using=client, index="course")
    #
    # # multi_match = MultiMatch(query=keywords, fields=["title", "description"])
    # q = Q("multi_match", query=keywords, fields=['title', 'description'])
    # # q = Q("match", title=keywords)
    #
    # # search = Search(using=client, index="course")
    #
    # # search.query(q)
    # search.from_dict({
    #     "query": {
    #         "multi_match": {
    #             "query": keywords,
    #             "fields": ["description"]
    #         }
    #     }
    # })
    #
    # response = search.execute(ignore_cache=True)
    # if not response.success():
    #     return failure("查询失败")
    #
    # return success(response.to_dict())


