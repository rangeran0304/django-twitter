from friendships.services import FriendshipServices
from newsfeeds.api.serializers import NewsFeedSerializer
from newsfeeds.models import NewsFeed

class NewsFeedService(object):
    # 整个newsfeed的逻辑是，当我们发帖时回通过fanout创建一个newsfeed
    # 然后用户运用views里面的list方法进行查看

    # 错误的方法
    # 不可以将数据库操作放在 for 循环里面，效率会非常低
    # for follower in FriendshipService.get_followers(tweet.user):
    #     NewsFeed.objects.create(
    #         user=follower,
    #         tweet=tweet,
    #     )

    # 正确的方法：使用 bulk_create，会把 insert 语句合成一条
    @classmethod
    def fanout_to_followers(cls,tweet):
        followers = FriendshipServices.get_followers(tweet.user)
        newsfeeds = [
            NewsFeed(user = follower, tweet = tweet)
            for follower in followers
        ]
    #发帖者本人也要看到这个帖子
        newsfeeds.append(NewsFeed(user= tweet.user, tweet = tweet))
        NewsFeed.objects.bulk_create(newsfeeds)
