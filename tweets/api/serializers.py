from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from tweets.models import Tweet
from accounts.api.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from comments.api.serializers import CommentSerializer
from likes.services import LikeService
from tweets.models import TweetPhoto
from tweets.constants import TWEET_PHOTO_UPLOAD_limit
from tweets.services import TweetService



# 用于请求成功之后返回相关信息
class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    photo_urls = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content','likes_count','has_liked','photo_urls')
    def get_likes_count(self,obj):
        return obj.like_set.count()
    def get_has_liked(self,obj):
        return LikeService.has_liked(self.context['request'].user,obj)
    def get_photo_urls(self,obj):
        photos_urls = []
        for photo in obj.tweetphoto_set.all().order_by('order'):
            photos_urls.append(photo.file.url)
        return photos_urls


class TweetSerializerWithComments(TweetSerializer):
    user = UserSerializer()
    comments = CommentSerializer(source='comment_set',many=True)
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content','comments','likes_count','has_liked','photo_urls')



# 创建Tweetcreate用以创建tweet
class TweetcreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)
    files = serializers.ListField(
        child = serializers.FileField(),
        allow_empty= True,
        required=False,
    )
    class Meta:
        model = Tweet
        fields = ('content','files')
    def validate(self,data):
        if len(data.get('files',[]))>TWEET_PHOTO_UPLOAD_limit:
            raise ValidationError({
                'message':f'you can not upload more than {TWEET_PHOTO_UPLOAD_limit} photos'
            })
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        if validated_data.get('files'):
            TweetService.create_photo_arrays_from_files(
                tweet = tweet,
                files = validated_data.get('files'),
            )
        return tweet