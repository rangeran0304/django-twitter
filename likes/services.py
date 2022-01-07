from likes.models import Like
from django.contrib.contenttypes.fields import ContentType

class LikeService(object):

    #write a method to see if the user has liked the target or not
    @classmethod
    def has_liked(cls,user,target):
        if user.is_anonymous:
            return False
        return Like.objects.filter(
            content_Type= ContentType.objects.get_for_model(target.__class__),
            object_id=target.id,
            user=user,
        ).exists()

