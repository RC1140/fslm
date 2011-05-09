from django.contrib import admin
from fslm.spacemanager.models import Drive,MediaType,FolderType,Folder,FolderAdmin,DriveAdmin,FolderTypeAdmin,MediaTypeAdmin

admin.site.register(Drive,DriveAdmin)
admin.site.register(MediaType,MediaTypeAdmin)
admin.site.register(Folder,FolderAdmin)
admin.site.register(FolderType,FolderTypeAdmin)
