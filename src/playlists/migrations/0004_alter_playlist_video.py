# Generated by Django 4.0 on 2021-12-31 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0013_alter_video_video_id'),
        ('playlists', '0003_playlist_videos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='featured_playlist', to='videos.video'),
        ),
    ]
