# Generated by Django 3.1.4 on 2020-12-25 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flavaudio', '0005_remove_audio_playlists'),
        ('flavplaylist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(to='flavaudio.Audio'),
        ),
    ]
