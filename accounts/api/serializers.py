from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        """"
        meta指的是配置信息,在user这个model里面取信息
        """""
        model = User
        fields = ['url', 'username', 'email']
