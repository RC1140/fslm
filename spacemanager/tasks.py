from celery.decorators import task
import shutil
import os.path
from models import *
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
        notifo.send_notification(settings.notifoUser,settings.notifoSecret,settings.notifoUser,('%s Moved successfully from %s to %s')%( mi.SourceFolder , mi.StartTime.strftime('%d %b %H:%M'),  mi.EndTime.strftime('%d %b %H:%M')))
        return 'Folder Moved'
    else:
        return 'No Queue Item Found'


@task()
def ping():
    print('pinged')
