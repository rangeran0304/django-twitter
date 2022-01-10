from django.test import TestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now
from friendships.services import FriendshipServices
from accounts.models import UserProfile

class Tweet_test(TestCase):

    def test_hour_to_now(self):
        test = User.objects.create_user(username='test')
        tweet1 = Tweet(user = test, content='test_time')
        tweet1.save()
        tweet1.created_at = utc_now() - timedelta(hours=10)
        self.assertEqual(tweet1.hours_to_now,10)

    def test_get_followers(self):
        print (FriendshipServices.get_followers(user=1))


from testing.testcase import TestCase
class UserProfileTests(TestCase):

    def test_profile_property(self):
        user1 = self.create_user('user1')
        self.assertEqual(UserProfile.objects.count(), 0)
        p = user1.profile
        self.assertEqual(isinstance(p, UserProfile), True)
        self.assertEqual(UserProfile.objects.count(), 1)
# Create your tests here.
