from rest_framework.test import APIClient
from testing.testcase import TestCase
from tweets.models import Tweet
from django.core.files.uploadedfile import SimpleUploadedFile
from tweets.models import TweetPhoto
# 注意要加 '/' 结尾，要不然会产生 301 redirect
TWEET_LIST_API = '/api/tweets/'
TWEET_CREATE_API = '/api/tweets/'
TWEET_RETRIVE_API = '/api/tweets/{}/'


class TweetApiTests(TestCase):

    def setUp(self):
        self.anonymous_client = APIClient()

        self.user1 = self.create_user('user1', 'user1@jiuzhang.com')
        self.tweets1 = [
            self.create_tweet(self.user1)
            for i in range(3)
        ]
        self.user1_client = APIClient()
        self.user1_client.force_authenticate(self.user1)

        self.user2 = self.create_user('user2', 'user2@jiuzhang.com')
        self.tweets2 = [
            self.create_tweet(self.user2)
            for i in range(2)
        ]

    def test_list_api(self):
        # 必须带 user_id
        response = self.anonymous_client.get(TWEET_LIST_API)
        self.assertEqual(response.status_code, 400)

        # 正常 request
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 3)
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user2.id})
        self.assertEqual(len(response.data['tweets']), 2)
        # 检测排序是按照新创建的在前面的顺序来的
        self.assertEqual(response.data['tweets'][0]['id'], self.tweets2[1].id)
        self.assertEqual(response.data['tweets'][1]['id'], self.tweets2[0].id)
    def test_create_api(self):
        # 必须登录
        response = self.anonymous_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 403)

        # 必须带 content
        response = self.user1_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 400)
        # content 不能太短
        response = self.user1_client.post(TWEET_CREATE_API, {'content': '1'})
        self.assertEqual(response.status_code, 400)
        # content 不能太长
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': '0' * 141
        })
        self.assertEqual(response.status_code, 400)

        # 正常发帖
        tweets_count = Tweet.objects.count()
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': 'Hello World, this is my first tweet!'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.user1.id)
        self.assertEqual(Tweet.objects.count(), tweets_count + 1)
    def test_retrive(self):
        # the tweet with id = -1 does not exist
        response = self.anonymous_client.get(TWEET_RETRIVE_API.format(-1))
        self.assertEqual(response.status_code,404)
        #test that it can get the comment of a tweet
        response = self.anonymous_client.get(TWEET_RETRIVE_API.format(self.tweets1[0].id))
        self.assertEqual(len(response.data['comments']),0)
        # test that you can get the right comment
        self.create_comment(self.user1,self.tweets1[0].id,'testtest')
        response = self.anonymous_client.get(TWEET_RETRIVE_API.format(self.tweets1[0].id))
        self.assertEqual(response.data['comments'][0]['content'], 'testtest')

    def test_like_set(self):
        self.create_like(self.user1,self.tweets1[0])
        self.assertEqual(self.tweets1[0].like_set.count(),1)
        self.create_like(self.user1, self.tweets1[0])
        self.assertEqual(self.tweets1[0].like_set.count(), 1)

    def test_tweet_with_photo(self):
        file = SimpleUploadedFile(
            name='selfie.jpg',
            content=str.encode('a fake image'),
            content_type='image/jpeg',
        )
        #test creating a tweet with empty file
        response = self.user1_client.post(TWEET_CREATE_API,{
            'content' : "123456789",
            'files' : [],
        })
        self.assertEqual(response.status_code,201)
        self.assertEqual(TweetPhoto.objects.count(),0)
        #test ceating a tweet with one file
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': "123456789",
            'files': [file],
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TweetPhoto.objects.count(), 1)
        #test creating a tweet with more than 9 files
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': "123456789",
            'files': [file,file,file,file,file,file,file,file,file,file,file,file],
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(TweetPhoto.objects.count(), 1)