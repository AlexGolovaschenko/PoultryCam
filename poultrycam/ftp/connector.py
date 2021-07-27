import pysftp
import os 
import io

from django.conf import settings

from photos.models import Photo, PhotoMetaData
from poultrycam.settings import SFTP_HOSTNAME, SFTP_USERNAME, SFTP_PASSWORD

from . import utils


# -----------------------------------------------------------------------------
class FtpConnector():
    def __init__(self):
        self.sftp = None

    def connect(self):
        if self.sftp is None:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            self.sftp = pysftp.Connection(SFTP_HOSTNAME, username=SFTP_USERNAME, password=SFTP_PASSWORD, cnopts=cnopts)
        return self.sftp        

    def close(self):
        if self.sftp is not None:
            self.sftp.close()
            self.sftp = None


    def scan_dir(self, dir='.', remove_empty_dirs=False):
        root = dir
        pathes = []
        print(f'scan dir {dir}')

        ld = self.sftp.listdir(dir)

        #remove empty dirs
        if remove_empty_dirs and (not ld):
            self._remove_empty_dir(dir)

        for d in ld:
            next = '/'.join((root, d))
            if self.sftp.isdir(next):
                res = self.scan_dir(next, remove_empty_dirs=True)
                for r in res:
                    if self.sftp.isfile(r):
                        pathes.append(r)
            elif self.sftp.isfile(next):
                pathes.append(next)
        return pathes


    def get_file_data(self, path):
        self.connect()
        try:
            with self.sftp.open(path, mode='r', bufsize=0) as f:
                data = f.read()
                self.close()
                return data
        except FileNotFoundError:
            print('Error: FileNotFoundError')
            self.close()
            return None

    def move_file(self, source_path, dest_path):
        self.connect()
        self.sftp.rename(source_path, dest_path)

    def remove_file(self, path):
        self.connect()
        if path:
            self.sftp.remove(path)

    def _remove_empty_dir(self, dir):
        if self.sftp.isdir(dir):
            print(f'empty dir removed {dir}')
            self.sftp.rmdir(dir)


 

# -----------------------------------------------------------------------------
class FtpPhotosStorageConnector():
    def __init__(self):
        self.ftp = FtpConnector()

    def close(self):
        self.ftp.close()

    def update_photos_list(self, dir='.'):
        self.ftp.connect()
        files = self.ftp.scan_dir(dir)
        photos_list = utils.select_jpg(files)
        self._relocate_photos_list_and_save_to_DB(photos_list)
        print('\n'.join(photos_list))
        self.ftp.close()


    def relocate_photo(self, photo, dir):
        source_path = os.path.normpath( photo.img.url.replace('/ftp-media/', '') ) # fix the problem with pathes on Windows
        source_path = os.path.join(settings.SFTP_STORAGE_ROOT, source_path)
        dest_path = source_path.replace('new', dir)
        self.ftp.move_file(source_path, dest_path)
        photo.img.name = dest_path.replace(settings.SFTP_STORAGE_ROOT, '')
        photo.save()


    def _relocate_photos_list_and_save_to_DB(self, pathes):
        for path in pathes:
            # save photo to DB
            self._save_photo_to_DB(path)
            # delete photo on ftp
            print(f'file removed {path}')
            self.ftp.remove_file(path)


    def _save_photo_to_DB(self, path):
        try:
            file_data = self.ftp.get_file_data(path)
            cam_name    = utils.parse_cam_name_from_path(path)
            cam_id      = utils.parse_cam_id_from_path(path)
            upload_data = utils.parse_date_from_path(path)
            upload_data_clear = utils.clear_upload_data(upload_data)
            photo_name = f'{cam_name}_{cam_id}_{upload_data_clear}'
            photo = Photo.objects.create(img='', title=f'{photo_name}.jpg')
            PhotoMetaData.objects.create(
                photo       = photo, 
                cam_name    = cam_name,
                cam_id      = cam_id,
                upload_data = upload_data,
                ftp_path    = path,
                )
            uploaded_file = io.BytesIO(file_data)
            uploaded_file.name = f'{photo_name}.jpg'
            photo.img.save(f'{photo_name}.jpg', uploaded_file, save=True)
            return photo
        except FileNotFoundError:
            print('Error: FileNotFoundError')
            return None




