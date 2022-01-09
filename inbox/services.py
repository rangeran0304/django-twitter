from django.contrib.contenttypes.fields import ContentType
from comments.models import Comment
from tweets.models import Tweet
from notifications.signals import notify

class NotificationServices(object):
    @classmethod
    def send_like_notification(cls,like):
        target_like = like.content_object
        if target_like.user == like.user:
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
                recipient = target_like.user,
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