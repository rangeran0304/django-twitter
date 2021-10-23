from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from tweets.models import Tweet
from accounts.api.serializers import UserSerializer


# 用于请求成功之后返回相关信息
class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')


# 创建Tweetcreate用以创建tweet
class TweetcreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)
    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet