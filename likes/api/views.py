from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from tweets.api.serializers import Tweet,TweetcreateSerializer,TweetSerializer,TweetSerializerWithComments
from likes.models import Like
from likes.api.serializers import LikeserializerForCreate, Likeserializer,LikeserializerForCancel
from newsfeeds.services import NewsFeedService
from utils.decorators import required_params
from rest_framework import status
from rest_framework.decorators import action

class LikeViewSet(viewsets.ModelViewSet):

    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LikeserializerForCreate

    @required_params(request_attr='data',params=['content_Type','object_id'])
    def create(self, request, *args, **kwargs,):
        serializer = LikeserializerForCreate(
            data = request.data,
            context = {'request':request}
        )
        if not serializer.is_valid():
             return Response(
                  {'message': 'please check input',
                  'errors': serializer.errors,
                  },status = status.HTTP_400_BAD_REQUEST
                   )
        instance = serializer.save()
        return Response(
            Likeserializer(instance).data,
            status=status.HTTP_201_CREATED,
        )
    @action(methods=['post'],detail=False)
    @required_params(request_attr='data', params=['content_Type', 'object_id'])
    def cancel(self, request, *args, **kwargs):
        serializer = LikeserializerForCancel(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
             return Response(
                  {'message': 'please check input',
                  'errors': serializer.errors,
                  },status = status.HTTP_400_BAD_REQUEST
                   )
        serializer.cancel()
        return Response(
            {
                    'success': 'True',
                    'message': 'You have cancelled your like'
            }, status=status.HTTP_200_OK
            )