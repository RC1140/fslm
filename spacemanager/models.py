from django.db import models
from django.contrib import admin

class Drive(models.Model):
    Path=models.CharField(max_length=1024)
    Name=models.CharField(max_length=255)

class MediaType(models.Model):    
    Name=models.CharField(max_length=255)

class FolderType(models.Model):    
    Name=models.CharField(max_length=255)
    MediaType=models.ForeignKey(MediaType)
    
class Folder(models.Model):
    Drive=models.ForeignKey(Drive)
    Type=models.ForeignKey(FolderType)
    Path=models.CharField(max_length=1024, default='')
    
class FolderAdmin(admin.ModelAdmin):
    search_fields = ['Path']
    list_display = ('Drive','Path','Type')
