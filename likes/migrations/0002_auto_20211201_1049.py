# Generated by Django 3.1.3 on 2021-12-01 10:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='contentType',
            new_name='content_Type',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'content_Type', 'object_id')},
        ),
        migrations.AlterIndexTogether(
            name='like',
            index_together={('content_Type', 'object_id', 'created_at')},
        ),
    ]
