import os
import shutil
from django.http import HttpResponse
from django.template import RequestContext, Template, Context
from django.shortcuts import *
from django.contrib.auth import logout
from datetime import date
from datetime import datetime
from lib import *
#from settings import LOG_FILE
from tasks import moveFolderBackground
from django.contrib.auth import login
from models import *
from django.forms.models import modelformset_factory
import logging


def logInfo(message):
#    logger = logging.getLogger(__name__)
#    hdlr = logging.FileHandler(LOG_FILE+ '/info.log')
#    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#    hdlr.setFormatter(formatter)
#    logger.addHandler(hdlr)
#    logger.setLevel(logging.INFO)
#    logger.info(message)
    return;




def logmeout(request):
    logout(request)
    return render_to_response('simpleMessage.html',{'title':'You have been logged out','message':'You have been successfully logged out!'}, context_instance=RequestContext(request))

def needsAuth(request):
    if getSetting('ForceLogin') == 'True':
       if request.user.is_authenticated():
           return None
       else:
           if request.path.startswith('/login'):
               return None
           return HttpResponseRedirect('/login/?next='+request.path)
    return None
    
def needsAuthUsr(user):
    if getSetting('ForceLogin') == 'True':
       if user.is_authenticated():
           return None
       else:
           return HttpResponseRedirect('/login/')
    return None
    
def getSetting(key=''):
    if Setting.objects.filter(SettingKey = key).count() != 0:
        return Setting.objects.filter(SettingKey = key)[0].Value
    return ''


def checkDriveOverMaxCapacity(disk):
    s = getSpace(disk.Path)
    cap = float(s['capacity'])
    used = float(s['used'])
    perc = (used / cap) * 100
    if perc > disk.MaxUsagePercentage:
        return True
    else:
        return False

def calcSize(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  #returns MB
    
def calcGBSize(start_path):
    return calcSize(start_path)/1024

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
        driveData += "{'name':'" + drive.Name + "', 'space':'" + k['available'].__str__() + "','capacity':'" + k['capacity'].__str__() + "','used':'" + k['used'].__str__() + "','isOver':'" + isOver.__str__() + "','link':'/drivestats/" + drive.id.__str__() + "','type':'"+ drive.DriveType +  "'},"
    driveData += ']'
    return HttpResponse(driveData)

def drivestats(request, drivepath):
    if (Drive.objects.filter(id=drivepath).count() == 0):
        return render_to_response('stats.html', context_instance=RequestContext(request))
    drive = Drive.objects.filter(id=drivepath)[0]
    isOver = checkDriveOverMaxCapacity(drive)
    overBy = getDriveOverMaxCapacity(drive)
    driveStats = getSpace(drive.Path)
    free = formatSpace(driveStats['available'])
    used = formatSpace(driveStats['used'])
    folders = drive.folder_set.all().order_by('Path')
    return render_to_response('stats.html', {'drive': drive, 'isOver': isOver,'free':free, 'used':used,  'overBy': overBy,  'folders':folders}, context_instance=RequestContext(request))

def getFirstAvailableDumpFolder(excludeFolder='',  monitorFolder=''):
    '''Should return a folder where files can be moved to 
        if none is found then a '' is returned and nothing should be
        moved , it might also be good to indicate this somewhere in the
        system.'''
    '''Get monitor folder type'''
    monitorMediaType = monitorFolder.MediaType
    if Drive.objects.filter(DriveType='D').count() == 0:
        logInfo('GFADF: No Dump Folders found')
        return {'path':'', 'drive':''}

    drives = Drive.objects.filter(DriveType='D').order_by('DumpPreference')

    if drives.count() > 0:
        logInfo('GFADF: '+ drives.count().__str__() + ' dump drives found')
        for d in drives:
            dumpFolders = d.folder_set.filter(MediaType=monitorMediaType).order_by('Path')
            logInfo('GFADF:DFF: '+dumpFolders.count().__str__() + 'Dump Folders found for ' + d.Name )
            s = getRawDriveOverMaxCapacity(d)
            if s < -1:
                logInfo('GFADF:OC: First Available Dump Drive: '+ d.Name +' Over Capacity:'+ s.__str__())
                #there is free space on this drive under the max capacity  and at least 1 gigabyte is free
                for dumpFolder in dumpFolders:
                    logInfo('First Available Dump Folder found: '+ dumpFolder.Path)
                    return {'path':dumpFolder.Path, 'drive':d}
            else: 
                logInfo('GFADF:OC: Dump Drive: '+ d.Name +' Over Capacity:'+ s.__str__()  + ' but still not less than -1?')
    logInfo('First Available Dump Folder not found')
    return {'path':'', 'drive':''}

def getSpaceToFree(monitorDrive, dumpDrive):
    excess = getDriveOverMaxCapacity(monitorDrive)
    vacuum = getDriveOverMaxCapacity(dumpDrive)
    if (vacuum > 0):
        return 0
    if (excess > vacuum):
        return excess
    else:
        return vacuum

def initQueue(request):
    if request.POST:
        #only load incomplete tasks
        queueLoader = MoveQueueItem.objects.filter(StartTime__gt=datetime.now())
        for item in queueLoader:
            moveFolderBackground.delay(item.id)
        return render_to_response('simpleMessage.html',{'title':'Items Queued','message':'Items Queued , as they are completed notifo messages will be sent'}, context_instance=RequestContext(request))
    else:
        return HttpResponse('GET Not Allowed')

def deleteQueueItem(request,queueid):
    queueid = int(queueid)
    MoveQueueItem.objects.get(id=queueid).delete()
    return render_to_response('simpleMessage.html',{'title':'Queue Item Deleted','message':'Queue Item Deleted'}, context_instance=RequestContext(request))

def viewDbQueue(request):
    itemsToCopy = MoveQueueItem.objects.filter(StartTime__gt=datetime.now())
    for item in itemsToCopy:
        item.PotentialSpaceFreed = formatSpace(item.PotentialSpaceFreed)
    return render_to_response('dbQueue.html',{'folders':itemsToCopy}, context_instance=RequestContext(request))

def viewActiveDbQueue(request):
    itemsBusyCopy = MoveQueueItem.objects.filter(StartTime__lt=datetime.now()).filter(EndTime__gt=datetime.now())
    for item in itemsBusyCopy:
        item.PotentialSpaceFreed = formatSpace(item.PotentialSpaceFreed)
        k = datetime.now() - item.StartTime
        item.Duration = k.seconds / 60 #minutes
    return render_to_response('dbActiveQueue.html',{'folders':itemsBusyCopy}, context_instance=RequestContext(request))

def settings(request):
    settings = Setting.objects.all()
    if request.method == "POST":
        for setting in settings:
            value =request.POST.get(setting.SettingKey)
            if value != "":
                setting.Value = value
                setting.save()
    else:
        settings = Setting.objects.all()
    return render_to_response("settings.html", {"settings": settings}, context_instance=RequestContext(request))

def moveFiles(request):
    if request.method == 'POST':
        ''' We dont actually move any folders here we just stick them in the db queue
               At some other point in time we can run through the queue and create
               the required tasks
        '''
        foldersToMove = request.session.get('folders',False)
        if foldersToMove:
            for folderConstruct in foldersToMove:
                moveID = request.POST.get(folderConstruct['id'].__str__(),False)
                if moveID:
                    mi = MoveQueueItem()
                    mi.SourceFolder = folderConstruct['source']
                    mi.DestFolder = folderConstruct['dest']
                    mi.PotentialSpaceFreed = unFormatSpace(folderConstruct['space'])
                    logInfo('Saving MoveQueueItem to the db, Source:'+mi.SourceFolder + ' ' + mi.DestFolder)
                    mi.StartTime = date(2050, 12, 31)
                    mi.EndTime = date(2050, 12, 31)
                    mi.save()
                    mi.StartTime = date(2050, 12, 31)
                    mi.EndTime = date(2050, 12, 31)
                    mi.save()
                    folderConstruct['moved'] = True
                else:
                    folderConstruct['moved'] = False
        request.session['folders'] = False
        return render_to_response('dataMoved.html',{'folders':foldersToMove}, context_instance=RequestContext(request))
    else:
        ignoreHidden = getSetting('IgnoreHidden')
        #This is a generic move request almost like what would happen in cron job
        drives = Drive.objects.filter(DriveType='M')
        #Some serious looping about to begin , this might be able to be optimized later
        if drives.count() == 0:
            #If no drives are found exit
            logInfo('Move: No Drives setup to monitor')
            return HttpResponse('No drives found to monitor')
        foldersQueued = []
        for monitorDrive in drives:
            logInfo('Move: Monitor drives found')
            freedSpace = 0
            spaceToFree = 0
            #print spaceToFree
            monitorFolders = monitorDrive.folder_set.all().order_by('Path')
            '''Get a list of drives that we are monitoring
                   Check if there are any folders that were defined for the drive and
                   if so start checking them as candidates to be moved'''
            if monitorFolders.count() != 0:
                for monitorFolder in monitorFolders:
                    scanFolders = os.listdir(monitorFolder.Path)
                    scanFolders.sort()
                    id = 0
                    for folder in scanFolders:
                        if (ignoreHidden == 'True' and not(folder.startswith('.'))) or (ignoreHidden != 'True'):
                            myfolder = os.path.join(monitorFolder.Path, folder)
                            if MoveQueueItem.objects.filter(SourceFolder=myfolder).count() == 0:
                                logInfo('Move: an existing MoveQueueItem was not found')
                                dump = getFirstAvailableDumpFolder(monitorFolder=monitorFolder)
                                firstAvailableFolder = dump['path']
                                dumpDrive = dump['drive']
                                '''If the size of the folder we are checking is smaller than the amount of
                                        space we need its ok to move the folder'''
                                if (dumpDrive != ''):
                                    '''we dont have to worry about it being a positive number
                                    because we are checking that firstavailablefolder is not
                                    nothing and it only returns folders that have extra space free'''
                                    spaceToFree = abs(getRawDriveOverMaxCapacity(dumpDrive))
                                    logInfo('Space to free: ' +spaceToFree.__str__() + 'MB')
                                else:
                                    logInfo('Move: DumpDrive recieved was empty')

                                if os.path.isdir(myfolder):
                                    logInfo('Move: the folder '+ myfolder + ' is a valid directory')
                                    folderSpace = calcSize(myfolder)
                                    logInfo('Folder'+myfolder+' Size: '+folderSpace.__str__()+ 'MB')
                                    if (freedSpace + folderSpace) <= spaceToFree:
                                        freedSpace += folderSpace
                                        '''Get a dump folder , check if one is found if so that use it for the copies
                                            Instead of adding directly to the db , we load into a list for processing later
                                        '''
                                        if firstAvailableFolder != '':
                                            id += 1
                                            foldersQueued.append({'id':id,
                                                                  'source':myfolder,
                                                                  'dest':os.path.join(firstAvailableFolder, folder),
                                                                  'space':formatSpace(calcSize(myfolder))})
                                        else:
                                            return HttpResponse('No Dump folders found')
                                else:
                                    logInfo('Move: the folder '+ myfolder + ' is a valid directory')
                                    folderSpace = os.path.getsize(myfolder) 
                                    logInfo('Folder'+myfolder+' Size: '+folderSpace.__str__()+ 'MB')
                                    if (freedSpace + folderSpace) <= spaceToFree:
                                        freedSpace += folderSpace
                                        '''Get a dump folder , check if one is found if so that use it for the copies
                                            Instead of adding directly to the db , we load into a list for processing later
                                        '''
                                        if firstAvailableFolder != '':
                                            id += 1
                                            foldersQueued.append({'id':id,
                                                                  'source':myfolder,
                                                                  'dest':os.path.join(firstAvailableFolder, folder),
                                                                  'space':formatSpace(calcSize(myfolder))})
                                        else:
                                            return HttpResponse('No Dump folders found')

                                    #Yes this is not a dir but we can still move or copy it
                                    logInfo('Move: the folder '+ myfolder + ' is not a valid directory')

    request.session['folders'] = foldersQueued
    return render_to_response('dataToBeMoved.html',{'folders':foldersQueued}, context_instance=RequestContext(request))
