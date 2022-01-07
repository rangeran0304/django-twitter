from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from tweets.api.serializers import Tweet,TweetcreateSerializer,TweetSerializer,TweetSerializerWithComments
from newsfeeds.services import NewsFeedService
from utils.decorators import required_params
from rest_framework import status


class TweetViewset(viewsets.GenericViewSet):

    queryset = Tweet.objects.all()
    serializer_class = TweetcreateSerializer


    # 重写list和create函数。

    # 获取权限的函数。根据不同的请求返回不同的权限
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    # 重写list方法。要求根据userid来列出表单。

    def retrieve(self, request, *args, **kwargs):
        if 'pre' in request.query_params \
                and request.query_params['pre']=='1':
            tweet = self.get_object()
            return Response(
                TweetSerializerWithComments(
                    tweet,
                    context= {'pre':True,'request':request,},
                ).data
            )
        else:
            tweet = self.get_object()
            return Response(
                  TweetSerializerWithComments(
                      tweet,
                      context={'pre': False,'request':request},
                  ).data
            )
    @required_params(params = ['user_id'])
    def list(self, request, *args, **kwargs):

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
        return Response({'tweets':serializer.data},status=status.HTTP_200_OK)

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
        NewsFeedService.fanout_to_followers(tweet)
        return Response(TweetSerializer(tweet).data,status=201)


