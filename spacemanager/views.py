# Create your views here.
import os
from django.http import HttpResponse

def getSpace(disk):
    s = os.statvfs(disk)
    capacity = s.f_bsize * s.f_blocks
    available = s.f_bsize * s.f_bavail
    used = s.f_bsize * (s.f_blocks - s.f_bavail)
    return (available / (1048576)) / 1000

def calcSize(start_path):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
	    for f in filenames:
		fp = os.path.join(dirpath, f)
		total_size += os.path.getsize(fp)
	return total_size / (1024 * 1024)

def moveFiles(request):
    '''This defines the monitor and dump folders , later we can add multiple so that 
    it can monitor many folders and dump to many folders as needed based on space '''
    monitorFolder = {'folder':'/downloads/complete/TV/','type':'series'}
    dumpFolder = {'folder':'/media/DownloadWing/Series/','type':'series'}
    files = os.listdir(monitorFolder['folder'])
    files.sort()
    smallestChunk = 9999999
    foldername = ''
    for folder in files:
	myfolder = os.path.join(monitorFolder['folder']+folder) 
	if os.path.isdir(myfolder):
		if calcSize(myfolder) < smallestChunk:
			smallestChunk = calcSize(myfolder)
			foldername = myfolder
		
    return HttpResponse('This smallest folder that can be moved and its size is '+foldername+' ' +smallestChunk.__str__())
