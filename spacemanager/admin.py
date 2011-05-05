from django.contrib import admin
from fslm.spacemanager.models import Drive
from fslm.spacemanager.models import MediaType
from fslm.spacemanager.models import FolderType
from fslm.spacemanager.models import Folder


admin.site.register(Drive)
admin.site.register(MediaType)
admin.site.register(FolderType)
admin.site.register(Folder)
