# Generated by Django 3.2.3 on 2021-05-28 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0010_auto_20210527_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photometadata',
            name='upload_data',
            field=models.DateTimeField(max_length=50, null=True, verbose_name='Дата и время сохренения изображения'),
        ),
    ]
