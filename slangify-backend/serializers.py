from rest_framework import serializers
from .models import Slang, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        
class SlangSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    generated_context = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Slang
        fields = ['id', 'term', 'meaning', 'category', 'category_id', 'origin', 'popularity', 'created_at', 
                  'usage_example', 'cultural_origin', 'trendiness_score', 'generated_context']