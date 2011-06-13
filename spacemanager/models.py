from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from datetime import datetime
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
    def __unicode__(self):
        return self.Name.__str__()
   
class Folder(models.Model):
    Drive=models.ForeignKey(Drive)
    Path=models.CharField(max_length=1024, default='')
    MediaType=models.ForeignKey(MediaType,  default=1)

class MoveQueueItem(models.Model):    
    ''' MoveQueueItem is used to indicate any folders that need to be moved
        Decided not to use the celery tables as they are not
        dependable (they require the events be turned on and
        this can be easily forgotten) '''
    SourceFolder = models.CharField(max_length=255,unique=True)
    DestFolder = models.CharField(max_length=1024)
    #space that can be freed by executing this item in mb
    PotentialSpaceFreed = models.IntegerField(default=0)
    StartTime = models.DateTimeField()
    EndTime = models.DateTimeField()


class Setting(models.Model):
    SettingKey = models.CharField(max_length=1024,null=True) 
    Value=models.CharField(max_length=1024,  default='')
    Type = models.CharField(max_length=100,  default='bool' )
    def __unicode__(self):
        return self.SettingKey.__str__() + ' ' + self.Value

class FolderAdmin(admin.ModelAdmin):
    search_fields = ['Path']
    list_display = ('Drive','Path', 'MediaType')

class DriveAdmin(admin.ModelAdmin):
    search_fields = ['Name','Path']
    list_display = ('Name','Path')

class MediaTypeAdmin(admin.ModelAdmin):
    search_fields = ['Name']
    list_display = ('Name','id')
class MoveQueueItemAdmin(admin.ModelAdmin):
    search_fields = ['SourceFolder']
    list_display = ('id','SourceFolder')
    
class SettingAdmin(admin.ModelAdmin):    
    search_fields= ['SettingKey']
    list_display = ('id', 'SettingKey', 'Value')
