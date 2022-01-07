from rest_framework import viewsets,status
from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from friendships.models import Friendships
from newsfeeds.api.serializers import NewsFeedSerializer
from newsfeeds.models import NewsFeed

class NewsFeedViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    #自定义get_queryset用来得到newsfeed
    #因为需要在登录情况下去获取该用户的newsfeed

    def get_queryset(self):
        return NewsFeed.objects.filter(user = self.request.user)

    def list(self,request):
        serializer = NewsFeedSerializer\
            (self.get_queryset(),context={'request':request},many=True)
        return Response({
            'newsfeeds': serializer.data
        },status= status.HTTP_200_OK)
