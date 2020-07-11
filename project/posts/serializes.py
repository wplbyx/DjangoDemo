from posts.models.article import Article
from rest_framework import serializers
from common.serializes import CustomListSerializer


#############################
# 创建 DRF Serialize 序列化器 #
#############################


class ArticleSerialize(serializers.ModelSerializer):
    """"""
    # updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 重新格式化时间

    class Meta:
        model = Article
        fields = ['uid', 'chapter', 'description', 'updated']
        read_only_fields = ['uid']
        list_serializer_class = CustomListSerializer  # 批量修改辅助类对象
        extra_kwargs = {
            "created": {
                "required": False,
                "format": "%Y-%m-%d %H:%M:%S"
            },
            "updated": {
                "required": False,
                "format": "%Y-%m-%d %H:%M:%S"
            }
        }
