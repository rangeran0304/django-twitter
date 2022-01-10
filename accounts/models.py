from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    avatar = models.FileField(null = True)
    nickname = models.CharField(null = True, max_length=200)
    signature = models.CharField(null=True,max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}{}{}'.format(self.user,self.nickname,self.signature)

    def get_profile(user):
        if hasattr(user,'_cached_user_profile'):
            return getattr('_cached_user_profile')
        userprofile,_ = UserProfile.objects.get_or_create(user=user)
        setattr(user,'_cached_user_profile',userprofile)
        return userprofile

    User.profile = property(get_profile)


