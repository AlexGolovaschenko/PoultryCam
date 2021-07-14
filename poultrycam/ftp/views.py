import os
from django.shortcuts import render
from django.http import HttpResponse


from .connector import FtpConnector

def ftp_media_view(request, path):
    path = os.path.normpath(path) # fix the problem with pathes on Windows
    ftp = FtpConnector()
    f = ftp.open_file('sorted/' + path)
    return HttpResponse( f, content_type='image/jpg' )