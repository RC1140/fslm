import os
import shutil
from django.http import HttpResponse
from django.template import RequestContext,Template,Context
from django.shortcuts import *
from tasks import moveFolderBackground
from models import Drive
   

def getSpace(disk):
    s = os.statvfs(disk)
    capacity = (s.f_bsize * s.f_blocks)/ (1048576)
    available = (s.f_bsize * s.f_bavail)/ (1048576)
    used = (s.f_bsize * (s.f_blocks - s.f_bavail) ) / (1048576)
    return  {'capacity': capacity,  'used':used, 'available': available}

def calcSize(start_path):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
	    for f in filenames:
		fp = os.path.join(dirpath, f)
		total_size += os.path.getsize(fp)
	return total_size / (1024 * 1024)

def smallestFolder(request):
    '''This defines the monitor and dump folders , later we can add multiple so that 
    it can monitor many folders and dump to many folders as needed based on space '''
    monitorFolder = {'folder':'/downloads/complete/TV/','type':'series'}
    dumpFolder = {'folder':'/media/DownloadWing/Series/','type':'series'}
    files = os.listdir(monitorFolder['folder'])
    files.sort()
    smallestChunk = 9999999
    foldername = ''
    for folder in files:
	myfolder = os.path.join(monitorFolder['folder'],folder) 
	if os.path.isdir(myfolder):
		if calcSize(myfolder) < smallestChunk:
			smallestChunk = calcSize(myfolder)
			foldername = myfolder
		
    return HttpResponse('This smallest folder that can be moved and its size is '+foldername+' ' +smallestChunk.__str__())

def home(request, callbacks):
    return render_to_response('home.html', context_instance=RequestContext(request))

def drivesList(request, callbacks):
	#get drives
        #getSpace('/media/Evo0') 
	drives = Drive.objects.all()
	driveData='['
	for drive in drives:
            k = getSpace(drive.Path)
            driveData += "{'name':'"+ drive.Name + "', 'space':'"+  k['available'].__str__() + "','capacity':'"+k['capacity'].__str__()+  "','used':'"+k['used'].__str__()+"'},"
        driveData += ']'
        return HttpResponse(driveData)

def moveFiles(request):
    #This is a generic move request almost like what would happen in cron job
    #If no drives are found exit 
    if Drive.objects.filter(DriveType='M').count() == 0:
        return HttpResponse('No Drives setup to monitor')
    
    spaceToFree = 2000

    monitorFolder = {'folder':'/downloads/complete/TV/','type':'series'}
    dumpFolder = {'folder':'/media/DownloadWing/Series/','type':'series'}

    drives = Drive.objects.filter(DriveType='M')
    #Some serious looping about to begin , this might be able to be optomized later
    for monitorDrive in drives:
        monitorFolders = monitorDrive.folder_set.all().order_by('Path')
        for monitorFolder in monitorFolders:
            scanFolders = os.listdir(monitorFolder.Path)
            folders.sort()

            smallestChunk = 9999999
            foldername = ''
            for folder in folders:
                myfolder = os.path.join(monitorFolder.Path,folder) 
                if os.path.isdir(myfolder):
                    if calcSize(myfolder) <= spaceToFree:
                        moveFolderBackground.delay(myfolder,os.path.join(dumpFolder['folder'],folder))
                        return HttpResponse('Moving in the background : '+myfolder)

    return HttpResponse('Nothing moved')
