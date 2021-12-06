from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Like(models.Model):
    object_id = models.PositiveIntegerField()
    content_Type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
    )
    content_object = GenericForeignKey(
        'content_Type',
        'object_id',
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    # must use the unique_index to avoid that a man like a tweet(or a content) twice
    # if you user filter, it might go wrong(concurrence)
    class Meta:
        unique_together = ('user','content_Type','object_id')
        index_together = ('content_Type','object_id','created_at')

    def __str__(self):
        return "at {}, {} liked {} {}".format(
            self.created_at,
            self.user,
            self.content_Type,
            self.object_id
         )


# Create your models here.
