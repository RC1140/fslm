from celery.decorators import task
import shutil
import os.path
from models import *
from lib import getDriveOverMaxCapacity
from lib import checkDriveOverMaxCapacity
import notifo
import settings
from datetime import datetime
@task()
def moveFolderBackground(moveQueueID):
    mi = MoveQueueItem.objects.get(id=int(moveQueueID))
    if mi:
        #set start time
        mi.StartTime = datetime.now()
        mi.save()
        #If the folder exists make a copy instead of a move
        if os.path.exists(mi.DestFolder):
            shutil.copy2(mi.SourceFolder, mi.DestFolder)
            shutil.rmtree(mi.SourceFolder)
        else:
            shutil.move(mi.SourceFolder,mi.DestFolder)
        
        #set the finish time instead of deleting
        mi.EndTime = datetime.now()
        mi.save()
        kbSaved = mi.PotentialSpaceFreed * 1024
        k = mi.EndTime - mi.StartTime
        rate = round(kbSaved / k.seconds)
        notifo.send_notification(settings.notifoUser,settings.notifoSecret,settings.notifoUser,('%s Moved successfully from %s to %s at an average rate of %s kb/s')%( mi.SourceFolder , mi.StartTime.strftime('%d %b %H:%M'),  mi.EndTime.strftime('%d %b %H:%M'), rate))
        return 'Folder Moved'
    else:
        return 'No Queue Item Found'

@task()
def notifyDrivesOverMaxCapacity():
    print('notifyDrivesOverMaxCapacity executed')
    if (Drive.objects.all().count() == 0):
        return
    for drive in Drive.objects.all():
        isOver = checkDriveOverMaxCapacity(drive)
        overBy = getDriveOverMaxCapacity(drive)
        if isOver:
            notifo.send_notification(settings.notifoUser,settings.notifoSecret,settings.notifoUser,('FSLM is notifying you that one of your managed drives: %s is over it\'s maximum capacity by overBy')%(drive.Name, overBy))
            return



@task()
def ping():
    print('pinged')
