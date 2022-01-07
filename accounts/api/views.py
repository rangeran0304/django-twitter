from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponse
from accounts.api.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth import(
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)
from accounts.api.serializers import SignupSerializer, LoginSerializer


def say_hello(request):
    return HttpResponse("helloworld")


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class AccountViewSet(viewsets.ViewSet):
    permission_classes =  (AllowAny,)
    serializer_class = SignupSerializer


    @action(methods=['post'], detail=False)
    def login(self,request):
        """
        登录方法，从request中获取账号密码。
        默认的username是admin，默认密码也是admin
        isvalid检测是否空。通过调用serializer.errors返回具体的errors。
        400表示是前端的错
        """
        serializer = LoginSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                "success":False,
                "message":"please check input",
                "errors":serializer.errors,
            },status=400)
        username1 = serializer.validated_data['username']
        password1 = serializer.validated_data['password']
        user = django_authenticate(username = username1, password = password1)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                'message': "username and password does not match"

            },status = 400)
        django_login(request,user)
        return Response({
            "success": True,
            "user":UserSerializer(instance = user).data,
        },status = 200)
    @action(methods=['post'],detail=False)
    def logout(self,rquest):
        """
        实现登出功能
        """
        django_logout(rquest)
        return Response({
            "success":True
        })


    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        user = serializer.save()
        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        }, status=201)
    @action (methods=['get'],detail=False)
    def login_status(self,request):
        data = {
            'if_logged_in':request.user.is_authenticated,
            'ip': request.META['REMOTE_ADDR'],
        }
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)