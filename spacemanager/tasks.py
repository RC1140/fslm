from celery.decorators import task
import shutil
import os.path
from models import *
import notifo
import settings

@task()
def moveFolderBackground(moveQueueID):
    mi = MoveQueueItem.objects.get(id=int(moveQueueID))
    if mi:
        #If the folder exists make a copy instead of a move
        if os.path.exists(mi.DestFolder):
            shutil.copy2(mi.SourceFolder, mi.DestFolder)
            shutil.rmtree(mi.SourceFolder)
        else:
            shutil.move(mi.SourceFolder,mi.DestFolder)
        notifo.send_notification(settings.notifoUser,settings.notifoSecret,settings.notifoUser,('%s Moved successfully')%( mi.SourceFolder ))
        mi.delete()
        return 'Folder Moved'
    else:
        return 'No Queue Item Found'
