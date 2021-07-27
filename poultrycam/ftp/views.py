import os
import io
from PIL import Image

from django.shortcuts import render
from django.http import HttpResponse
from poultrycam.settings import MEDIA_ROOT


from .connector import FtpConnector

def ftp_media_view(request, path):
    path = os.path.normpath(path) # fix the problem with pathes on Windows
    ftp = FtpConnector()
    f = ftp.get_file_data('sorted/' + path)

    # resizing image
    img_width = request.GET.get('width', None)
    img_height = request.GET.get('height', None)
    if img_width or img_height:
        image_file = io.BytesIO(f)
        with Image.open(image_file) as image:
            w, h = image.size
            if not img_width:
                img_width = w
            if not img_height:
                img_height = h   
            size = (int(img_width), int(img_height))       
            image.thumbnail(size)
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                f = output.getvalue()    

    response = HttpResponse(f, content_type='image/jpg' )
    response['Content-Disposition'] = 'filename="image.jpg"'
    return response



def local_media_view(request, path):
    # open image
    with open(MEDIA_ROOT + path, "r") as file:
        f = file.read()

    # resizing image
    img_width = request.GET.get('width', None)
    img_height = request.GET.get('height', None)
    if img_width or img_height:
        image_file = io.BytesIO(f)
        with Image.open(image_file) as image:
            w, h = image.size
            if not img_width:
                img_width = w
            if not img_height:
                img_height = h   
            size = (int(img_width), int(img_height))       
            image.thumbnail(size)
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                f = output.getvalue()    

    response = HttpResponse(f, content_type='image/jpg' )
    response['Content-Disposition'] = 'filename="image.jpg"'
    return response









