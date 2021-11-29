from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from comments.models import Comment
from tweets.models import Tweet
from accounts.api.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    User = UserSerializer
    class Meta:
        model = Comment
        fields = ('id','Tweet_id','User','content','created_at','updated_at')


class CommentSerializerForCreate(serializers.ModelSerializer):
    Tweet_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('content','Tweet_id')

    def validate(self,data):
        tweet_id = data['tweet_id']
        if not Tweet.objects.filter(id = tweet_id).exists():
            raise ValidationError({'message':'the tweet you comment at does not exist'})
        return data
    def create(self,validate_data):
        user = self.context['request'].user
        comment = Comment.objects.create(
            Tweet_id=validate_data['tweet_id'],
            content=validate_data['content'],
            User=user,
        )
        return comment

class CommentSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)
    #when the instance is not none when you call .save, you will update the instance
    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.save()
        return instance