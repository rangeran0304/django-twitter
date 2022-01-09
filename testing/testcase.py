from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from comments.models import Comment
from django.contrib.contenttypes.fields import ContentType
from likes.models import Like
from rest_framework.test import APIClient

COMMENT_URL = '/api/comments/'
LIKE_URL = '/api/likes/'
NOTIFICATION_URL = '/api/notifications/'
class TestCase(DjangoTestCase):

    anonymous_client = APIClient()
    def create_user(self, username, email='test@test.com', password=None):
        if password is None:
            password = 'generic password'
        # 不能写成 User.objects.create()
        # 因为 password 需要被加密, username 和 email 需要进行一些 normalize 处理
        return User.objects.create_user(username, email, password)

    def create_tweet(self, user, content=None):
        if content is None:
            content = 'default tweet content'
        return Tweet.objects.create(user=user, content=content)

    def create_comment(self,user,tweet_id,content=None):
        if content is None:
            content = 'default comment content'
        return Comment.objects.create(User = user, Tweet_id = tweet_id, content=content)

    def create_like(self,user,target):
        contentType = ContentType.objects.get_for_model(target.__class__)
        instance,_ = Like.objects.get_or_create(user=user,content_Type=contentType,object_id=target.id)
        return instance
    def create_user_and_client(self, *args, **kwargs):
        user = self.create_user(*args, **kwargs)
        client = APIClient()
        client.force_authenticate(user)
        return user, client

    def post_comment(self,client,tweet_id,content=None):
        if content == None:
            client.post('/api/comments/',
                        {
                            'Tweet_id': tweet_id,
                            'content': 'default comment'
                        }

                        )
            return

        client.post('/api/comments/',
                    {
                        'Tweet_id' : tweet_id,
                        'content': content
                    }

        )
        return

    def post_tweet_like(self, client, target,):
            client.post(LIKE_URL,
                        {
                            'content_Type': 'tweet',
                            'object_id':target.id,
                        }

                        )
            return