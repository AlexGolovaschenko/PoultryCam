# Generated by Django 3.2.3 on 2021-05-27 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0009_auto_20210527_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='photometadata',
            name='cam_id',
            field=models.CharField(blank=True, max_length=50, verbose_name='Идентификатор камеры'),
        ),
        migrations.AddField(
            model_name='photometadata',
            name='upload_data',
            field=models.CharField(blank=True, max_length=50, verbose_name='Дата и время сохренения изображения'),
        ),
    ]
