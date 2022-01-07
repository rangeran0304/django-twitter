from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from tweets.models import Tweet
from accounts.api.serializers import UserSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comment
from comments.api.serializers import CommentSerializer
from likes.services import LikeService



# 用于请求成功之后返回相关信息
class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content','likes_count','has_liked')
    def get_likes_count(self,obj):
        return obj.like_set.count()
    def get_has_liked(self,obj):
        return LikeService.has_liked(self.context['request'].user,obj)


class TweetSerializerWithComments(TweetSerializer):
    user = UserSerializer()
    comments = CommentSerializer(source='comment_set',many=True)
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content','comments','likes_count','has_liked')



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