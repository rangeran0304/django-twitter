from notifications.models import Notification
from testing.testcase import TestCase
from likes.models import Like

COMMENT_URL = '/api/comments/'
LIKE_URL = '/api/likes/'
NOTIFICATION_URL = '/api/notifications/'

class NotificationTests(TestCase):

    def setUp(self):
        self.user1, self.user1_client = self.create_user_and_client('user1')
        self.user2, self.user2_client = self.create_user_and_client('user2')
        self.user1_tweet = self.create_tweet(self.user1)

    def test_comment_trigger_notification(self):
        self.assertEqual(Notification.objects.count(),0)
        self.post_comment(client=self.user2_client,tweet_id=self.user1_tweet.id)
        self.assertEqual(Notification.objects.count(), 1)

    def test_like_trigger_notification(self):
        self.assertEqual(Notification.objects.count(), 0)
        self.post_tweet_like(client=self.user2_client,target=self.user1_tweet)
        self.assertEqual(Like.objects.count(),1)
        self.assertEqual(Notification.objects.count(), 1)

class NotificationApiTests(TestCase):
    def setUp(self):
        self.user1, self.user1_client = self.create_user_and_client('user1')
        self.user2, self.user2_client = self.create_user_and_client('user2')
        self.user1_tweet = self.create_tweet(self.user1)

    def test_unread_test(self):
        url = '/api/notifications/unread-count/'
        response = self.user1_client.get(url)
        self.assertEqual(response.data['unread_count'],0)
        self.post_tweet_like(self.user2_client,self.user1_tweet)
        response = self.user1_client.get(url)
        self.assertEqual(response.data['unread_count'], 1)
        self.post_comment(self.user2_client,tweet_id=self.user1_tweet.id)
        response = self.user1_client.get(url)
        self.assertEqual(response.data['unread_count'], 2)
        self.assertEqual(response.status_code,200)

    def test_mark_all_as_read(self):
        url = '/api/notifications/unread-count/'
        response = self.user1_client.get(url)
        self.assertEqual(response.data['unread_count'], 0)
        self.post_tweet_like(self.user2_client, self.user1_tweet)
        self.post_comment(self.user2_client, tweet_id=self.user1_tweet.id)
        response = self.user1_client.get(url)
        self.assertEqual(response.data['unread_count'], 2)
        url2 = '/api/notifications/mark-all-as-read/'
        response = self.user1_client.post(url2)
        self.assertEqual(response.data['updated_count'], 2)
        self.assertEqual(response.status_code,201)
        response = self.user1_client.get(url)
        self.assertEqual(response.data['unread_count'], 0)

    def test_list(self):
        self.post_tweet_like(self.user2_client, self.user1_tweet)
        self.post_comment(self.user2_client, tweet_id=self.user1_tweet.id)
        #anonymous can not access
        response = self.anonymous_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code,403)
        #user2 can not get the notifications for user1
        response = self.user2_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'],0)
        #user1 can get 2 notifications
        response = self.user1_client.get(NOTIFICATION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_update(self):
        url = '/api/notifications/unread-count/'
        self.post_tweet_like(self.user2_client, self.user1_tweet)
        self.post_comment(self.user2_client, tweet_id=self.user1_tweet.id)
        response = self.user1_client.get(url)
        self.assertEqual(response.data['unread_count'], 2)
        url2 = '/api/notifications/1/'
        response = self.user1_client.put(url2,{'unread':False})
        response = self.user1_client.get(url)
        self.assertEqual(response.data['unread_count'], 1)