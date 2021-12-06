from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from django.contrib.contenttypes.fields import ContentType
from likes.models import Like
from accounts.api.serializers import UserSerializer
from comments.models import Comment
from tweets.models import Tweet
from rest_framework.exceptions import ValidationError
class Likeserializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Like
        fields = ('user','created_at')

#Since we must be logged in to like something
#So we can just get our user by context
class BaseLikeserializer(serializers.ModelSerializer):
    content_Type = serializers.CharField()

    class Meta:
        model = Like
        fields = ('content_Type', 'object_id')

    def _get_model_class(self, data):
        type = data['content_Type']
        if type == 'comment':
            return Comment
        if type == 'tweet':
            return Tweet
        return None

    def validate(self, data):
        model_type = self._get_model_class(data)
        if model_type == None:
            raise ValidationError({'content_Type': 'must provide valid content_Type'})
        id = data['object_id']
        if not model_type.objects.filter(id=id).exists():
            raise ValidationError({'object_id': 'must provide valid object_id'})
        return data
class LikeserializerForCreate(BaseLikeserializer):

    def create(self,validated_data):
        model_type = self._get_model_class(validated_data)
        instance, _ = Like.objects.get_or_create(
            user=self.context['request'].user,
            content_Type=ContentType.objects.get_for_model(model_type),
            object_id=validated_data['object_id']
        )
        return instance
class LikeserializerForCancel(BaseLikeserializer):
    def cancel(self):
        model_type = self._get_model_class(self.validated_data)
        return Like.objects.filter(
                user=self.context['request'].user,
                content_Type=ContentType.objects.get_for_model(model_type),
                object_id=self.validated_data['object_id']
                ).delete()