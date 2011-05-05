from celery.decorators import task
import shutil
import os.path

@task()
def add(x, y):
        return x + y

@task()
def moveFolderBackground(sourceFolder, destFolder):
    #If the folder exists make a copy instead of a move
    if os.path.exists(destFolder):
        shutil.copy2(sourceFolder, destFolder)
        shutil.rmtree(sourceFolder)
    else:
        shutil.move(sourceFolder,destFolder)
    return 'Moved folder '+ sourceFolder +' to '+ destFolder
