from django.contrib import admin
from likes.models import Like

@admin.register(Like)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_Type', 'object_id','user', 'created_at')
    date_hierarchy = 'created_at'

# Register your models here.
