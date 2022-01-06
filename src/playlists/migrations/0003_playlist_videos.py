# Generated by Django 4.0 on 2021-12-31 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0013_alter_video_video_id'),
        ('playlists', '0002_playlist_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(blank=True, related_name='playlist_item', to='videos.Video'),
        ),
    ]