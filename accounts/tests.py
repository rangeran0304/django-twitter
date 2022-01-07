from django.test import TestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now
from friendships.services import FriendshipServices

class Tweet_test(TestCase):

    def test_hour_to_now(self):
        test = User.objects.create_user(username='test')
        tweet1 = Tweet(user = test, content='test_time')
        tweet1.save()
        tweet1.created_at = utc_now() - timedelta(hours=10)
        self.assertEqual(tweet1.hours_to_now,10)

    def test_get_followers(self):
        print (FriendshipServices.get_followers(user=1))
# Create your tests here.
