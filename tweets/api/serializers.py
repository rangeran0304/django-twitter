from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from tweets.models import Tweet
from accounts.api.serializers import UserSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comment
from comments.api.serializers import CommentSerializer



# 用于请求成功之后返回相关信息
class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')

class TweetSerializerWithComments(serializers.ModelSerializer):
    user = UserSerializer()
    #comments = CommentSerializer(source='comment_set',many=True)
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content','comments')

    def get_comments(self,obj):
        comments = [
            comment.content
            for comment in Comment.objects.filter(Tweet_id=obj.id)
        ]
        if self.context['pre']:
            return comments[0:2]
        return comments


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