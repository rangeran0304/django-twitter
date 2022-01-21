from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now
from django.contrib.contenttypes.fields import ContentType
from likes.models import Like
from tweets.constants import Tweet_Photo_Status_Choices,TweetPhotoStatus

# 建立联合索引，并配置排序配置
# 首先根据user排序再根据createdat排序。-代表降序


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def hours_to_now(self):
        # django中datetimefield自带的是UTC时间。我们新建一个time_helpers文件来得到现在的UTC时间。并相减
        return (utc_now()-self.created_at).seconds//3600

    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at')

    def __str__(self):
        return f'created at {self.created_at} by {self.user} : {self.content}'

    @property
    def like_set(self):
        return Like.objects.filter(
            content_Type = ContentType.objects.get_for_model(Tweet),
            object_id = self.id
        ).order_by('created_at')

# Create your models here.
class TweetPhoto(models.Model):
    # set the tweet and user as the forign key to suggest teh tweet and user the
    # photo belongs to
    tweet = models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    # the photo itself
    file = models.FileField()
    # the order of the photo
    order = models.IntegerField(default = 0)
    #the status of the photo//used for censoring
    status = models.IntegerField(
        default = TweetPhotoStatus.PENDING,
        choices = Tweet_Photo_Status_Choices,
    )
    # we use the soft delete in the photo model,
    # which means rather than the photo will be deleted from the database
    # we will mark it as 'deleted'
    has_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null =True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            ('user','created_at'),
            ('file','created_at'),
            ('has_deleted','created_at'),
            ('tweet','created_at'),
        )
    def __str__(self):
        return f'{self.tweet_id}:{self.file}'


