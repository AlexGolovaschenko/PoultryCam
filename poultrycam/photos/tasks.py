
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger

from ftp.connector import FtpPhotosStorageConnector


logger = get_task_logger(__name__)

@shared_task(name = "update_photos_list")
def update_photos_list():
    logger.info('Started photo list updating')

    ftp = FtpPhotosStorageConnector()
    logger.info('Connection to FTP has done')

    ftp.update_photos_list('inbox')
    ftp.close()
    logger.info('Photo list updated')


