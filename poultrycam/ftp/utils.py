import re
from datetime import datetime
from django.utils.timezone import make_aware


# return the file paths who has .jpg extension
def select_jpg(files):
    return [f for f in files if re.search(r'.jpg$', f)]


# parse data from file path
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


# parse factory id of camera from file path
def parse_cam_id_from_path(path):
    results = re.search(r'inbox/cam\d+/(\w+)/', path)
    if results:
        return results.group(1)
    else:
        return None


# parse camera name from file path
def parse_cam_name_from_path(path):
    results = re.search(r'inbox/(cam\d+)/', path)
    if results:
        return results.group(1)
    else:
        return None


# prepare date time string for add to file name
def clear_upload_data(dt):
    return dt.strftime(r'%Y_%m_%d_%H_%M_%S')
