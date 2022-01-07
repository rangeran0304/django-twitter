from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from tweets.api.serializers import Tweet,TweetcreateSerializer,TweetSerializer

class TweetViewset(viewsets.GenericViewSet):

    queryset = Tweet.objects.all()
    serializer_class = TweetcreateSerializer

    # 重写list和create函数。

    # 获取权限的函数。根据不同的请求返回不同的权限
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]
    # 重写list方法。要求根据userid来列出表单。

    def list(self, request, *args, **kwargs):
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)
        # 这句查询会被翻译为
        # select * from twitter_tweets
        # where user_id = xxx
        # order by created_at desc
        # 这句 SQL 查询会用到 user 和 created_at 的联合索引
        # 单纯的 user 索引是不够的
        tweets = Tweet.objects.filter(
            user_id = request.query_params['user_id']).order_by(
            '-created_at'
        )
        serializer = TweetSerializer(instance=tweets, many=True)
        # 一般来说 json 格式的 response 默认都要用 hash 的格式
        # 而不能用 list 的格式（约定俗成）
        return Response({'tweets':serializer.data})

    # 重写create方法。将当前登录的user传入serializer
    # 利用request将user信息传入给serializer
    def create(self, request, *args, **kwargs):
        serializer = TweetcreateSerializer(
            data= request.data,
            context= {'request':request},

        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        tweet = serializer.save()
        return Response(TweetcreateSerializer(tweet).data,status=201)


