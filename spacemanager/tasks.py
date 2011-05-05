from celery.decorators import task
import shutil

@task()
def add(x, y):
        return x + y

@task()
def moveFolderBackground(sourceFolder, destFolder):
        shutil.move(sourceFolder,destFolder)
        return 'Moved folder '+ sourceFolder +' to '+ destFolder
