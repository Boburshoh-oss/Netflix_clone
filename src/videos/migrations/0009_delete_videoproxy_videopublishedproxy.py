# Generated by Django 4.0 on 2021-12-28 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_videoallproxy'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VideoProxy',
        ),
        migrations.CreateModel(
            name='VideoPublishedProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Published Video',
                'verbose_name_plural': 'Published Videos',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('videos.video',),
        ),
    ]
