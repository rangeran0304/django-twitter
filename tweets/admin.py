from django.contrib import admin
from tweets.models import Tweet,TweetPhoto


@admin.register(TweetPhoto)
class TweetPhotoAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'user',
        'tweet',
        'file',
        'has_deleted',
    )
class TweetPhotoInline(admin.StackedInline):
    model = TweetPhoto
    can_delete = False
    verbose_name_plural = 'tweet_photos'
@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (
        'created_at',
        'user',
        'content',
    )
    inlines = (TweetPhotoInline,)


# Register your models here.
