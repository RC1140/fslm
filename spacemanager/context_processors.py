from django.conf import settings
from views import needsAuthUsr

def theme_page(context):
    k = needsAuthUsr(context.user)
    if k:
        return {'THEME': settings.THEME,  'AUTHNEEDED':'TRUE'}	
    else:
        return {'THEME': settings.THEME}	
