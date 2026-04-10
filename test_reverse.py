import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','setup.settings')
import django
django.setup()
from django.urls import reverse, NoReverseMatch
try:
    print('logout ->', reverse('logout'))
except Exception as e:
    print('reverse error:', type(e).__name__, e)
try:
    print("core:logout ->", reverse('core:logout'))
except Exception as e:
    print('reverse core:logout error:', type(e).__name__, e)
