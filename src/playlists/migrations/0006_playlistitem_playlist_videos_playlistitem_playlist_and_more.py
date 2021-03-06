# Generated by Django 4.0 on 2022-01-02 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0013_alter_video_video_id'),
        ('playlists', '0005_remove_playlist_videos'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['order', 'timestamp'],
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(blank=True, related_name='playlist_item', through='playlists.PlayListItem', to='videos.Video'),
        ),
        migrations.AddField(
            model_name='playlistitem',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlists.playlist'),
        ),
        migrations.AddField(
            model_name='playlistitem',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video'),
        ),
    ]
