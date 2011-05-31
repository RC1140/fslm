import os
import shutil
from django.http import HttpResponse
from django.template import RequestContext, Template, Context
from django.shortcuts import *
from tasks import moveFolderBackground
from models import *

def getSpace(disk):
    s = os.statvfs(disk)
    capacity = (s.f_bsize * s.f_blocks) / (1048576)
    available = (s.f_bsize * s.f_bavail) / (1048576)
    used = (s.f_bsize * (s.f_blocks - s.f_bavail) ) / (1048576)
    return  {'capacity': capacity, 'used': used, 'available': available}


def checkDriveOverMaxCapacity(disk):
    s = getSpace(disk.Path)
    cap = float(s['capacity'])
    used = float(s['used'])
    perc = (used / cap) * 100
    if perc > disk.MaxUsagePercentage:
        return True
    else:
        return False


def formatDriveSpace(kb):
    '''If Its more than 10 change it to the next format'''
    format = "KB"
    if (kb > 10240):
        kb = kb / 1024
        format = "MB"
        if (kb > 10240):
            kb = kb / 1024
            format = "GB"
            if (kb > 10240):
                kb = kb / 1024
                format = "TB"
    kb = round(kb, 2)

    return kb.__str__() + format


def getDriveOverMaxCapacity(disk):
    #something is wrong here i think
    s = getSpace(disk.Path)
    cap = float(s['capacity'])
    used = float(s['used'])
    perc = (used / cap) * 100
    if perc > disk.MaxUsagePercentage:
        capacitySize = cap * (float(disk.MaxUsagePercentage) / 100)
        over = used - capacitySize
        return formatDriveSpace(over)
    return 0


def calcSize(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)


def smallestFolder(folderToCheck):
    '''This defines the monitor and dump folders , later we can add multiple so that 
    it can monitor many folders and dump to many folders as needed based on space '''
    files = os.listdir(folderToCheck)
    files.sort()
    smallestChunk = 9999999
    foldername = ''
    for checkFile in files:
        myfolder = os.path.join(folderToCheck, checkFile)
        if os.path.isdir(myfolder):
            if calcSize(myfolder) < smallestChunk:
                smallestChunk = calcSize(myfolder)
                foldername = myfolder
    if foldername != '':
        return (foldername, smallestChunk)
    else:
        return ''
        #return HttpResponse('This smallest folder that can be moved and its size is '+foldername+' ' +smallestChunk.__str__())


def home(request, callbacks):
    return render_to_response('home.html', context_instance=RequestContext(request))


def drivesList(request, callbacks):
    #get drives
    #getSpace('/media/Evo0') 
    drives = Drive.objects.all()
    driveData = '['
    for drive in drives:
        k = getSpace(drive.Path)
        isOver = checkDriveOverMaxCapacity(drive)
        driveData += "{'name':'" + drive.Name + "', 'space':'" + k['available'].__str__() + "','capacity':'" + k['capacity'].__str__() + "','used':'" + k['used'].__str__() + "','isOver':'" + isOver.__str__() + "','link':'/drivestats/" + drive.id.__str__() + "'},"
    driveData += ']'
    return HttpResponse(driveData)


def drivestats(request, drivepath):
    if (Drive.objects.filter(id=drivepath).count() == 0):
        return render_to_response('stats.html', context_instance=RequestContext(request))
    drive = Drive.objects.filter(id=drivepath)[0]
    isOver = checkDriveOverMaxCapacity(drive)
    overBy = getDriveOverMaxCapacity(drive)
    return render_to_response('stats.html', {'drive': drive, 'isOver': isOver, 'overBy': overBy})


def getFirstAvailableDumpFolder(excludeFolder):
    '''Should return a folder where files can be moved to 
        if none is found then a '' is returned and nothing should be
        moved , it might also be good to indicate this somewhere in the
        system.'''
    if Drive.objects.filter(DriveType='D').count() == 0:
        return ''

    if excludeFolder:
        drives = Drive.objects.filter(DriveType='D').order_by('DumpPreference')
    else:
        drives = Drive.objects.filter(DriveType='D').order_by('DumpPreference')

    '''TODO : We need to indicate when a folder is full to prevent a drive
    from being over used'''
    if drives.count() > 0:
        for d in drives:
            monitorFolders = d.folder_set.all().order_by('Path')
            for monFolder in monitorFolders:
                spaceAvailable = getSpace(monFolder.Path)['available']
                spaceAvailable = spaceAvailable / 1000
                #You need to at least have a gig free space
                if spaceAvailable > 1:
                    return monFolder.Path
    else:
        return ''
        #for drive in drives:
        #freespace = calcSize(drive.Path)


def moveFiles(request):
    #This is a generic move request almost like what would happen in cron job
    #If no drives are found exit 
    if Drive.objects.filter(DriveType='M').count() == 0:
        return HttpResponse('No Drives setup to monitor')
        #todo use getDriveOverMaxCapacity to get amount of space needed
    

    spaceToFree = 2000

    drives = Drive.objects.filter(DriveType='M')
    #Some serious looping about to begin , this might be able to be optimized later
    for monitorDrive in drives:
        spaceToFree = getDriveOverMaxCapacity(monitorDrive)
        print spaceToFree
        monitorFolders = monitorDrive.folder_set.all().order_by('Path')
        '''Get a list of drives that we are monitoring 
               Check if there are any folders that were defined for the drive and
               if so start checking them as candidates to be moved'''
        for monitorFolder in monitorFolders:
            scanFolders = os.listdir(monitorFolder.Path)
            scanFolders.sort()
            smallestChunk = 9999999
            foldername = ''

            for folder in scanFolders:
                myfolder = os.path.join(monitorFolder.Path, folder)
                if os.path.isdir(myfolder):
                    '''If the size of the folder we are checking is smaller than the amount of
                        space we need its ok to move the folder'''
                    if calcSize(myfolder) <= spaceToFree:
                        '''Get a dump folder , check if one is found if so that use it for the copies'''
                        firstAvailableFolder = getFirstAvailableDumpFolder()
                        if firstAvailableFolder != '':
                            mi = MoveQueueItem()
                            mi.SourceFolder = myfolder
                            mi.DestFolder = os.path.join(firstAvailableFolder, folder)
                            mi.PotentialSpaceFreed = calcSize(myfolder)
                            mi.save()
                            moveFolderBackground.delay(mi.id)
                            return HttpResponse('Moving in the background : ' + myfolder)
                        else:
                            return HttpResponse('No Dump folders found')
    return HttpResponse('Nothing moved')
