# Generated by Django 3.2.3 on 2021-05-27 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_photo_photos_phot_marker_b57e03_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='marker',
            field=models.CharField(choices=[('NEW', 'Новый'), ('GOOD', 'Хорошо'), ('BAD', 'Плохо'), ('SKIP', 'Пропущен')], default='NEW', max_length=50, verbose_name='Метка'),
        ),
    ]
