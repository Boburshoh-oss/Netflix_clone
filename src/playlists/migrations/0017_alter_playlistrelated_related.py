# Generated by Django 4.0 on 2022-01-10 09:00

from django.db import migrations, models
import django.db.models.deletion
import playlists.models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0016_playlistrelated_playlist_related_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlistrelated',
            name='related',
            field=models.ForeignKey(limit_choices_to=playlists.models.pr_limit_choices_to, on_delete=django.db.models.deletion.CASCADE, related_name='related_item', to='playlists.playlist'),
        ),
    ]
