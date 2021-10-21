from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def hours_to_now(self):
        #django中datetimefield自带的是UTC时间。我们新建一个time_helpers文件来得到现在的UTC时间。并相减
        return (utc_now()-self.created_at).seconds//3600

    def __str__(self):
        return f'created at {self.created_at} by {self.user} : {self.content}'


# Create your models here.
