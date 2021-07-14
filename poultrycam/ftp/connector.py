import pysftp
import re
from datetime import datetime

from django.utils.timezone import make_aware
from photos.models import Photo, PhotoMetaData
from poultrycam.settings import SFTP_HOSTNAME, SFTP_USERNAME, SFTP_PASSWORD

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

    def update_photos_list(self, dir='.'):
        self.connect()
        files = self.scan_dir(dir)
        photos_list = select_jpg(files)
        self.relocate_photos(photos_list)
        print('\n'.join(photos_list))
        self.close()

    def scan_dir(self, dir='.', remove_empty_dirs=False):
        root = dir
        pathes = []
        print(f'scan dir {dir}')

        ld = self.sftp.listdir(dir)

        #remove empty dirs
        if remove_empty_dirs and (not ld):
            self.remove_empty_dir(dir)

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

    def remove_empty_dir(self, dir):
        if self.sftp.isdir(dir):
            print(f'empty dir removed {dir}')
            self.sftp.rmdir(dir)

    def relocate_photos(self, pathes):
        for path in pathes:
            # save photo to DB
            self.save_new_photo(path)
            # delete photo on ftp
            print(f'file removed {path}')
            self.sftp.remove(path)

    def save_new_photo(self, path, remove=False):
        try:
            with self.sftp.open(path, mode='r', bufsize=0) as f:
                photo = Photo.objects.create(img='', title='image')
                PhotoMetaData.objects.create(
                    photo       = photo, 
                    cam_name    = parse_cam_name_from_path(path),
                    cam_id      = parse_cam_id_from_path(path),
                    upload_data = parse_date_from_path(path),
                    ftp_path    = path,
                    )
                photo.img.save('image.jpg', f, save=True)
            return photo
        except FileNotFoundError:
            # do your FileNotFoundError code here
            print('Error: FileNotFoundError')
            return None

    def open_file(self, path):
        self.connect()
        try:
            with self.sftp.open(path, mode='r', bufsize=0) as f:
                data = f.read()
                self.close()
                return data
        except FileNotFoundError:
            # do your FileNotFoundError code here
            print('Error: FileNotFoundError')
            self.close()
            return None

# ----------------------------------------------------------------------------------------------
# Utils

def select_jpg(files):
    return [f for f in files if re.search(r'.jpg$', f)]



# string example:
# inbox/cam1/6M07E3EPAGC7C0F/2021-05-28/001/jpg/09/30.20[R][0@0][0].jpg
def parse_date_from_path(path):
    results = re.search(r'inbox/cam\d+/\w+/(\d\d\d\d-\d\d-\d\d)/001/jpg/(\d\d)/(\d\d).(\d\d)\[R\]\[0@0\]\[0\].jpg$', path)
    if results:
        str_date = results.group(1)
        str_hours = results.group(2)
        str_minutes = results.group(3)
        str_seconds = results.group(4)
        dt = datetime.strptime(' '.join((str_date, str_hours, str_minutes, str_seconds)),  r'%Y-%m-%d %H %M %S')
        return make_aware(dt)
    else:
        return None

def parse_cam_id_from_path(path):
    results = re.search(r'inbox/cam\d+/(\w+)/', path)
    if results:
        return results.group(1)
    else:
        return None

def parse_cam_name_from_path(path):
    results = re.search(r'inbox/(cam\d+)/', path)
    if results:
        return results.group(1)
    else:
        return None
