from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from friendships.models import Friendships
from accounts.api.serializers import UserserializerForFollower

class FriendshipSerializerForCreate(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()

    class Meta:
        model = Friendships
        fields = ('from_user_id', 'to_user_id')

    def validate(self,attrs):
        if attrs['from_user_id'] == attrs['to_user_id']:
            raise ValidationError({
                'message': 'you can not follow yourself'
            })

        if Friendships.objects.filter(
            from_user_id = attrs['from_user_id'],
            to_user_id = attrs['to_user_id']
        ).exists():
            raise ValidationError({
                'message': 'You can not follow the same person twice'
            })


        return attrs

    def create(self, validated_data):
        from_user_id = validated_data['from_user_id']
        to_user_id = validated_data['to_user_id']
        return Friendships.objects.create(
            from_user_id= from_user_id,
            to_user_id= to_user_id,
        )


class FollowerSerializer(serializers.ModelSerializer):

    user = UserserializerForFollower(source= 'from_user')
    created_at = serializers.DateTimeField()

    class Meta:
        model = Friendships
        fields = ('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):

    user = UserserializerForFollower(source= 'to_user')
    created_at = serializers.DateTimeField()

    class Meta:
        model = Friendships
        fields = ('user', 'created_at')
