from rest_framework import serializers
from news.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article model to convert to/from JSON.
    """
    class Meta:
        model = Article
        fields = '__all__'