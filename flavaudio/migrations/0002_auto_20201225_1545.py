# Generated by Django 3.1.4 on 2020-12-25 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flavaudio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='img_url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='audio',
            name='src_url',
            field=models.URLField(),
        ),
    ]
