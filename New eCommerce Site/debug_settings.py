import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print(f"BASE_DIR: {settings.BASE_DIR} type: {type(settings.BASE_DIR)}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"DATABASES: {settings.DATABASES}")
