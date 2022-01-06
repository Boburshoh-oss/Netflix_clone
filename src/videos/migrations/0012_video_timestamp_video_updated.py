# Generated by Django 4.0 on 2021-12-30 05:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_video_publish_timestamp_alter_video_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
