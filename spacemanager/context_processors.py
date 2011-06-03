from django.conf import settings

def theme_page(context):
    return {'THEME': settings.THEME}	
