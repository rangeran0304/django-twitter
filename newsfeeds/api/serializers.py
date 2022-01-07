from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from newsfeeds.models import NewsFeed
from tweets.api.serializers import TweetSerializer


class NewsFeedSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer()
    class Meta:
        model = NewsFeed
        fields = ('id','user','created_at','tweet')