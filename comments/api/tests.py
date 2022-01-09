from rest_framework.test import APIClient
from testing.testcase import TestCase
from tweets.models import Tweet
from django.utils import timezone


COMMENT_URL = '/api/comments/'

class CommentApiTests(TestCase):

    def setUp(self):
        self.test1 = self.create_user('test1')
        self.test1_Client = APIClient()
        self.test1_Client.force_authenticate(self.test1)
        self.test2 = self.create_user('test2')
        self.test2_Client = APIClient()
        self.test2_Client.force_authenticate(self.test2)
        self.tweet1 = self.create_tweet(self.test1,'this is a test')
        self.anonymous_client = APIClient()

    def test_create(self):
        #you can not comment if you dont log in
        response = self.anonymous_client.post(COMMENT_URL)
        self.assertEqual(response.status_code,403)
        #you can not comment witiout any args
        response = self.test1_Client.post(COMMENT_URL)
        self.assertEqual(response.status_code, 400)
        #you can not comment with no content
        response = self.test1_Client.post(COMMENT_URL,{'tweet_id':self.tweet1.id})
        self.assertEqual(response.status_code, 400)
        #you can not comment without tweet_id
        response = self.test1_Client.post(COMMENT_URL,{'content':'this is a test'})
        self.assertEqual(response.status_code, 400)
        #you can not comment a too long sentence
        response = self.test1_Client.post(COMMENT_URL
                , {'tweet_id':self.tweet1.id,'content': '1'*150})
        self.assertEqual(response.status_code, 400)
        self.assertEqual('content'in response.data['errors'],True)
        #a successful comment
        response = self.test1_Client.post(COMMENT_URL
                                         , {'Tweet_id': self.tweet1.id, 'content': 'successful test'})
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data['User'], self.test1.id)
        self.assertEqual(response.data['Tweet_id'], self.tweet1.id)
        self.assertEqual(response.data['content'],'successful test')
    def test_update(self):
        comment = self.create_comment(self.test1, self.tweet1.id, 'original')
        another_tweet = self.create_tweet(self.test2)
        url = '{}{}/'.format(COMMENT_URL, comment.id)

        # 使用 put 的情况下
        # 匿名不可以更新
        response = self.anonymous_client.put(url, {'content': 'new'})
        self.assertEqual(response.status_code, 403)
        # 非本人不能更新
        response = self.test2_Client.put(url, {'content': 'new'})
        self.assertEqual(response.status_code, 403)
        comment.refresh_from_db()
        self.assertNotEqual(comment.content, 'new')
        # 不能更新除 content 外的内容，静默处理，只更新内容
        before_updated_at = comment.updated_at
        before_created_at = comment.created_at
        now = timezone.now()
        response = self.test1_Client.put(url, {
            'content': 'new',
            'User_id': self.test2.id,
            'Tweet_id': another_tweet.id,
            'created_at': now,
        })
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'new')
        self.assertEqual(comment.User, self.test1)
        self.assertEqual(comment.Tweet, self.tweet1)
        self.assertEqual(comment.created_at, before_created_at)
        self.assertNotEqual(comment.created_at, now)
        self.assertNotEqual(comment.updated_at, before_updated_at)

    def test_list(self):
        # you cant get a list without tweet_id
        reponse = self.anonymous_client.get(COMMENT_URL)
        self.assertEqual(reponse.status_code,400)
        #you can get a list with tweet_id
        #at first, you have 0 comments
        reponse = self.anonymous_client.get(COMMENT_URL,{
            'Tweet_id':self.tweet1.id
        })
        self.assertEqual(len(reponse.data['comments']),0)
        #the list you get will be ordered by created_time
        self.create_comment(self.test1,self.tweet1.id,'1')
        self.create_comment(self.test1, self.tweet1.id, '11')
        self.create_comment(self.test1, self.tweet1.id, '111')
        reponse = self.anonymous_client.get(COMMENT_URL, {
            'Tweet_id': self.tweet1.id
        })
        self.assertEqual(len(reponse.data['comments'][0]['content']), 1)
        self.assertEqual(len(reponse.data['comments'][1]['content']), 2)
        self.assertEqual(len(reponse.data['comments'][2]['content']), 3)
