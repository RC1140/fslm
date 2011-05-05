# Create your views here.
import os
from django.http import HttpResponse

def getSpace(disk):
    s = os.statvfs(disk)
    capacity = s.f_bsize * s.f_blocks
    available = s.f_bsize * s.f_bavail
    used = s.f_bsize * (s.f_blocks - s.f_bavail)
    return (available / (1048576)) / 1000

def moveFiles(request):
    '''This defines the monitor and dump folders , later we can add multiple so that 
    it can monitor many folders and dump to many folders as needed based on space '''
    monitorFolder = {'folder':'/downloads/complete/TV/','type':'series'}
    dumpFolder = {'folder':'/media/DownloadWing/Series/','type':'series'}
    files = os.listdir(monitorFolder['folder'])
    return HttpResponse(sum([os.path.getsize(f) for f in os.listdir(files[0]) if os.path.isfile(f)]))
