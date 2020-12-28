# Generated by Django 3.1.4 on 2020-12-25 15:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('img_url', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=60)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]