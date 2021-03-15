import os 
from celery import Celery 
# Set default Django settings 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings') 
app = Celery('proj')   
# Celery will apply all configuration keys with defined namespace  
app.config_from_object('django.conf:settings', namespace='CELERY')   
app.conf.enable_utc = False # so celery doesn't take utc by default
app.autodiscover_tasks()