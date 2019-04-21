import os
from celery import Celery

os.environ.setdefault( 'DJANGO_SETTINGS_MODULE' , 'md5_light.settings' )
app = Celery( 'md5_light' )
app.config_from_object( 'django.conf:settings' , namespace = 'CELERY' ) 
app.autodiscover_tasks() 
