from django.db import models
from django.contrib.auth.models import User


class Friendships(models.Model):

    # set_null表示当user被删除的时候，这条记录并不会被删除
    # 而是将from_user或者时to_user设置为null
    # 由于from_user和to_user都是使用的外键，
    # 所以当我们从user跨关系查询时设置relatedkey来进行区分。
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='following_user_set'
    )
    to_user = models.ForeignKey(
        User,
        # set_null表示当删除时，外键属性设为null
        on_delete=models.SET_NULL,
        null=True,
        related_name='follower_user_set'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        index_together= (
            ('from_user_id','created_at'),
            ('to_user_id','created_at')
        )
        unique_together=(
            ('from_user_id','to_user_id')
        )

        # .format后将元素填到前面
        # 这计划将在print时显示
        def __str__(self):
            return '{} followed {}'.format(self.from_user_id, self.to_user_id)