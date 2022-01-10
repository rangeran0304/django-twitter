from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated, AllowAny
from tweets.api.serializers import Tweet,TweetcreateSerializer,TweetSerializer
from newsfeeds.services import NewsFeedService
from comments.api.serializers import CommentSerializer,CommentSerializerForCreate,CommentSerializerForUpdate
from comments.api.permissions import IsObjectOwner
from comments.models import Comment
from inbox.services import NotificationServices
from utils.decorators import required_params

class CommentViewSet(viewsets.GenericViewSet):
    serializer_class = CommentSerializerForCreate
    queryset = Comment.objects.all()
    #instead of creating a filterset, we can bypass by using filterset_fields
    filterset_fields = ('Tweet_id',)
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'update':
            return ([IsObjectOwner()])
        return [AllowAny()]

    @required_params(params = ['Tweet_id',])
    def list(self,request,*args,**kargs):
        queryset = self.get_queryset()
        comments = self.filter_queryset(queryset)
        return Response(
            {'comments':CommentSerializer(
                comments,
                context={'request':request},
                many=True).data,
             }
            ,status=status.HTTP_200_OK
        )

    def create(self,request,*args,**kargs):
        data = {
            'Tweet_id':request.data.get('Tweet_id'),
            'content':request.data.get('content'),
        }

        serializer = CommentSerializerForCreate(
            data=data,
            context= {'request':request},
        )
        if not serializer.is_valid():
            return Response({
                'message':'Please check input',
                'errors':serializer.errors,
            },status=status.HTTP_400_BAD_REQUEST)
        comment = serializer.save()
        NotificationServices.send_comment_notification(comment)
        commentSerializer = \
            CommentSerializer(comment,
                            context={'request':request})
        return  Response(
            commentSerializer.data,
            status = status.HTTP_201_CREATED)

    def update(self,request,*args,**kargs):
        serializer = CommentSerializerForUpdate(
            instance=self.get_object(),
            data = request.data,
        )
        if not serializer.is_valid():
            return Response(
                {
                    'message':'please check input',
                    'errors': serializer.errors,
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        comment = serializer.save()
        commentSerializer = \
            CommentSerializer(comment,
                              context={'request': request})
        return Response(
            commentSerializer.data,
            status = status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):

        comment = self.get_object()
        comment.delete()
        # DRF 里默认 destroy 返回的是 status code = 204 no content
        # 这里 return 了 success=True 更直观的让前端去做判断，所以 return 200 更合适
        return Response({'success': True}, status=status.HTTP_200_OK)