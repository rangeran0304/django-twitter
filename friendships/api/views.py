from rest_framework import viewsets,status
from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponse
from accounts.api.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from friendships.models import Friendships
from friendships.api.serializers import FollowerSerializer
from friendships.api.serializers import FollowingSerializer, FriendshipSerializerForCreate
from django.contrib.auth.models import User

class FriendshipsViewSet(viewsets.GenericViewSet):

    # 当访问POST的方法时必须要指定serializer——class，不然会报错
    serializer_class = FriendshipSerializerForCreate
    queryset = User.objects.all().order_by('-date_joined')
    @action(methods=['GET'],detail=True,permission_classes=[AllowAny])
    def followers(self,request,pk):
        friendships = Friendships.objects.filter(to_user_id= pk).order_by('-created_at')
        serializer = FollowerSerializer (friendships, many = True)
        return Response({
            'followers': serializer.data
        },status= status.HTTP_200_OK, )

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followings(self,request,pk):
        friendships = Friendships.objects.filter(from_user_id= pk).order_by('-created_at')
        serializer = FollowingSerializer (friendships, many = True)
        return Response({
            'followings': serializer.data
        },status= status.HTTP_200_OK, )


    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self,request,pk):
        # 判定是否关注的是不存在的用户
        self.get_object()
        # 判定是否已经关注了某人，或是进行了重复的follow操作,进行静默操作
        if Friendships.objects.filter(from_user_id = request.user, to_user_id= pk).exists():
            return Response({
                'success': True,
                'duplicate': True,
            },status= status.HTTP_201_CREATED,)
        serializer = FriendshipSerializerForCreate(
            data = {
                'from_user_id': request.user.id,
                'to_user_id': pk,
            }
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST, )
        serializer.save()
        return Response({
                'success': True,
            },status= status.HTTP_201_CREATED,)


    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self,request,pk):
        #pk实际上是str，需要转型
        if request.user.id == int(pk):
            return Response({
                'success': False,
                'message': 'you can not unfollow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not Friendships.objects.filter(from_user_id = request.user, to_user_id= pk).exists():
            return Response({
                'success': True,
                'deleted': False,
            }, status=status.HTTP_201_CREATED)
        # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#delete
        # Queryset 的 delete 操作返回两个值，一个是删了多少数据，一个是具体每种类型删了多少
        # 为什么会出现多种类型数据的删除？因为可能因为 foreign key 设置了 cascade 出现级联
        # 删除，也就是比如 A model 的某个属性是 B model 的 foreign key，并且设置了
        # on_delete=models.CASCADE, 那么当 B 的某个数据被删除的时候，A 中的关联也会被删除。
        # 所以 CASCADE 是很危险的，我们一般最好不要用，而是用 on_delete=models.SET_NULL
        # 取而代之，这样至少可以避免误删除操作带来的多米诺效应。
        deleted, _ = Friendships.objects.filter(
            from_user=request.user,
            to_user=pk,
        ).delete()
        return Response({'success': True, 'deleted': deleted})



    def list(self,request):
        return Response({
            'message':'this the home page of friendships'
        })