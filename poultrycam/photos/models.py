from django.db import models
from datetime import date

MARKER_NEW = 'NEW'
MARKER_GOOD = 'GOOD'
MARKER_BAD = 'BAD'
MARKER_SKIP = 'SKIP'

MARKER_CHOICES = [
    (MARKER_NEW, 'Новый'), 
    (MARKER_GOOD, 'Хорошо'), 
    (MARKER_BAD, 'Плохо'), 
    (MARKER_SKIP, 'Пропущен'), 
    ]

BAD_MARKER_DETAIL_CHOICES = [
    ('HIGH_TEMP', 'Высокая температура'), 
    ('LOW_TEMP', 'Низкая температура'), 
    ('OTHER', 'Другое'), 
    ]


def photo_upload_path(instance, filename):
    try:
        pmeta = PhotoMetaData.objects.get(photo =instance)
        cam_name = pmeta.cam_name
    except:
        cam_name = 'cam'
    return 'photos/{2}/{0}/{1}'.format(cam_name, filename, date.today().strftime("%Y/%m/%d"))


class Photo(models.Model):
    title = models.CharField(verbose_name='Имя файла', max_length=100)
    upload_date = models.DateTimeField(verbose_name='Дата добавления', auto_now=False, auto_now_add=True)
    img = models.ImageField(upload_to=photo_upload_path, default='default.png')

    marker = models.CharField(verbose_name='Метка', max_length=50, choices=MARKER_CHOICES, default=MARKER_NEW)
    bad_marker_detail = models.CharField(verbose_name='Уточнение плохой метки', max_length=50, choices=BAD_MARKER_DETAIL_CHOICES, blank=True)
    bad_marker_text = models.TextField(verbose_name='Другая причина', blank=True)

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

        indexes = [
            models.Index(fields=['marker',]),
        ]

    def __str__(self):
        return 'Photo (%s): %s' %(self.id, self.title)



class PhotoMetaData(models.Model):
    photo = models.OneToOneField(Photo, verbose_name='Фотография', on_delete=models.CASCADE)
    cam_name = models.CharField(verbose_name="Камера", max_length=50)
    ftp_path = models.TextField(verbose_name="Путь на ftp сервере", blank=True)
    cam_id = models.CharField(verbose_name="Идентификатор камеры", max_length=50, blank=True)
    upload_data = models.DateTimeField(verbose_name="Дата и время сохренения изображения", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Дополнительная информация"
        verbose_name_plural = "Дополнительная информация"