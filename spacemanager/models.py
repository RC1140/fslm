from django.db import models
from django.contrib import admin

class Drive(models.Model):
    Path=models.CharField(max_length=1024)
    Name=models.CharField(max_length=255)
    Drive_Types = (
        ('D','Dump'),
        ('M','Monitor'),
    )
    DriveType = models.CharField(max_length=1,choices=Drive_Types,null=True) 
    #For Dump drives we need to know maximum space usage as a %
    MaxUsagePercentage = models.IntegerField(default=80)
    '''For Monitor drives we need to know the ideal space usage as a % 
       the app will try to reach this but depending on free space on 
       the dump drives this might not be possible'''
    IdealFreeSpacePercentage = models.IntegerField(default=50)
    #If the user wants they can specify which drive to use first
    DumpPreference = models.IntegerField(default=0)

    def __unicode__(self):
	return self.DriveType.__str__() + ' ' + self.Name

class MediaType(models.Model):    
    Name=models.CharField(max_length=255, default='')

class FolderType(models.Model):    
    Name=models.CharField(max_length=255)
    MediaType=models.ForeignKey(MediaType)
    
class Folder(models.Model):
    Drive=models.ForeignKey(Drive)
    Type=models.ForeignKey(FolderType)
    Path=models.CharField(max_length=1024, default='')

class MoveQueueItem(models.Model):    
    ''' MoveItemQueue is used to indicate any folders that need to be moved
        Decided not to use the celery tables as they are not
        dependable (they require the events be turned on and
        this can be easily forgotten) '''
    SourceFolder = models.CharField(max_length=255,unique=True)
    DestFolder = models.CharField(max_length=1024)
    #space that can be freed by executing this item in mb
    PotentialSpaceFreed = models.IntegerField(default=0)

class FolderAdmin(admin.ModelAdmin):
    search_fields = ['Path']
    list_display = ('Drive','Path','Type')

class DriveAdmin(admin.ModelAdmin):
    search_fields = ['Name','Path']
    list_display = ('Name','Path')

class FolderTypeAdmin(admin.ModelAdmin):
    search_fields = ['Name']
    list_display = ('Name','MediaType')

class MediaTypeAdmin(admin.ModelAdmin):
    search_fields = ['Name']
    list_display = ('Name','id')
