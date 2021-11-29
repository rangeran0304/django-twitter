from friendships.models import Friendships

class FriendshipServices(object):

    # 错误的写法一
    # 这种写法会导致 N + 1 Queries 的问题
    # 即，filter 出所有 friendships 耗费了一次 Query
    # 而 for 循环每个 friendship 取 from_user 又耗费了 N 次 Queries
    # friendships = Friendship.objects.filter(to_user=user)
    # return [friendship.from_user for friendship in friendships]

    # 错误的写法二
    # 这种写法是使用了 JOIN 操作，让 friendship table 和 user table 在 from_user
    # 这个属性上 join 了起来。join 操作在大规模用户的 web 场景下是禁用的，因为非常慢。
    # friendships = Friendship.objects.filter(
    #     to_user=user
    # ).select_related('from_user')
    # return [friendship.from_user for friendship in friendships]

    # 正确的写法一，自己手动 filter id，使用 IN Query 查询
    # friendships = Friendship.objects.filter(to_user=user)
    # follower_ids = [friendship.from_user_id for friendship in friendships]
    # followers = User.objects.filter(id__in=follower_ids)

    # 正确的写法二，使用 prefetch_related，会自动执行成两条语句，用 In Query 查询
    # 实际执行的 SQL 查询和上面是一样的，一共两条 SQL Queries
    # cls表示这是类方法。可以不实例化直接调用

    #使用prefetch_related可以优化查询效率。不必要一次一次重复查询
    @classmethod
    def get_followers(cls,user):
        friendshipss = Friendships.objects.filter(to_user_id= user).prefetch_related('from_user')
        return [friendships.from_user for friendships in friendshipss]