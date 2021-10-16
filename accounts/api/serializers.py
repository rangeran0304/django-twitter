from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        """"
        meta指的是配置信息,定制一些行为规范
        """""
        model = User
        fields = ['username', 'email']
"""
signup中使用
"""
class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20,min_length=6)
    password = serializers.CharField(max_length=20,min_length=6)
    email = serializers.EmailField
    class Meta:
        """"
        meta指的是配置信息,定制一些行为规范
        """""

        model = User
        fields = ['username', 'email', 'password']
    #validate函数会在serilizer.is_valid调用
    def validate(self,data):
        if User.objects.filter(username = data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': 'This username has been occupied.'
            })
        if User.objects.filter(email = data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'email': 'This email address has been occupied.'
            })
        return data

    def create(self, validated_data):
        Username = validated_data['username'].lower()
        Email = validated_data['email'].lower()
        Password = validated_data['password']

        user = User.objects.create_user(
             username=Username,
             email=Email,
             password=Password,
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
       username = data['username'].lower()
       if not User.objects.filter(username = username).exists():
           raise exceptions.ValidationError({
               'username': 'User does not exist'
           })
       data['username'] = username
       return data