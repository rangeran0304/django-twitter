"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
routers(一种路由机制)实际上就是viewset对象的url映射关系提取出来。
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from accounts.api.views import UserViewSet,AccountViewSet
from tweets.api.views import TweetViewset
from django.conf import settings
from friendships.api.views import FriendshipsViewSet
from newsfeeds.api.views import NewsFeedViewSet
from comments.api.views import CommentViewSet
from likes.api.views import LikeViewSet
from inbox.api.views import NotificationviewSet


router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/accounts', AccountViewSet, basename='accounts')
router.register(r'api/tweets', TweetViewset, basename='tweets')
router.register(r'api/friendships', FriendshipsViewSet, basename='Friendships')
router.register(r'api/newsfeeds', NewsFeedViewSet, basename='NewsFeeds')
router.register(r'api/comments', CommentViewSet, basename='comments')
router.register(r'api/likes', LikeViewSet, basename='likes')
router.register(r'api/notifications', NotificationviewSet, basename='notifications')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
