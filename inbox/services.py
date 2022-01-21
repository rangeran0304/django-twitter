from django.contrib.contenttypes.fields import ContentType
from comments.models import Comment
from tweets.models import Tweet
from notifications.signals import notify
from django.contrib.contenttypes.fields import ContentType

class NotificationServices(object):
    @classmethod
    def send_like_notification(cls,like):
        target_like = like.content_object
        if target_like.__class__ == ContentType.objects.get_for_model(Tweet):
            if target_like.user == like.user:
                return
        if target_like.__class__ == ContentType.objects.get_for_model(Comment):
            if target_like.User == like.user:
                return
        if like.content_Type == ContentType.objects.get_for_model(Tweet):
            notify.send(
                like.user,
                recipient = target_like.user,
                actor = like.user,
                verb = 'liked your tweet',
                target = target_like,
            )
        if like.content_Type == ContentType.objects.get_for_model(Comment):
            notify.send(
                like.user,
                recipient = target_like.User,
                actor = like.user,
                verb = 'liked your comment',
                target = target_like,
            )

    @classmethod
    def send_comment_notification(cls,comment):
        if comment.User == comment.Tweet.user:
            return
        notify.send(
            comment.User,
            recipient=comment.Tweet.user,
            actor=comment.User,
            verb='comment on your tweet',
            target=comment,
        )