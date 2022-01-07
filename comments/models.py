from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet


class Comment(models.Model):
    User = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    Tweet = models.ForeignKey(Tweet,null=True,on_delete=models.SET_NULL)
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = (('Tweet_id','created_at'),)

    def __str__(self):
        return 'at {}, user {} comment {} on tweet {}'.format(
            self.created_at,
            self.User,
            self.content,
            self.Tweet,
        )
