from rest_framework import serializers

from web.models import CustomUser, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "name", "surname")

class ArticlesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    create_date = serializers.DateTimeField()
    user = UserSerializer()
    tags = TagSerializer(many=True)