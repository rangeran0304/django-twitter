from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import Notification
from rest_framework import  viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from inbox.api.serializers import NotificationSerializer, NotificationSerializerForUpdate
from utils.decorators import required_params


class NotificationviewSet(viewsets.GenericViewSet,viewsets.mixins.ListModelMixin):
     serializer_class = NotificationSerializer
     permission_classes = (IsAuthenticated,)
     filterset_fields = ('unread',)

     def get_queryset(self):
         #recipient(related:notifications) is the forign key of the notifications
         return self.request.user.notifications.all()

     @action(methods=['get'],detail=False,url_path='unread-count')
     def unread_count(self,request,*args,**kwargs):
         count_number = self.get_queryset().filter(unread = True).count()
         return Response(
             {'unread_count':count_number},
             status=status.HTTP_200_OK
         )

     @action(methods=['post'], detail=False, url_path='mark-all-as-read')
     def mark_all_as_read(self,request,*args,**kwargs):
         updated_count = self.get_queryset().filter(unread = True).update(unread = False)
         return Response(
             {'updated_count': updated_count},
             status=status.HTTP_201_CREATED
         )

     @required_params(method='PUT',params=['unread'])
     def update(self,request,*args,**kwargs):
         target = self.get_object()
         serializer= NotificationSerializerForUpdate(
             instance= target,
             data = request.data
         )
         if not serializer.is_valid():
             return Response(
                 {'message':'please check input',
                  'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST
             )
         notification = serializer.save()
         return Response(
              NotificationSerializer(notification).data,
              status = status.HTTP_200_OK
         )




