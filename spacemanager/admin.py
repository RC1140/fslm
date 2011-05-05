from django.contrib import admin
from fslm.spacemanager.models import Drive,MediaType,FolderType,Folder,FolderAdmin

admin.site.register(Drive)
admin.site.register(MediaType)
admin.site.register(FolderType)
admin.site.register(Folder,FolderAdmin)
