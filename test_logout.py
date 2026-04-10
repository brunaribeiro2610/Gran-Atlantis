import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','setup.settings')
import django
django.setup()
from django.test import Client
c = Client()
resp = c.get('/accounts/logout/')
print('status_code:', resp.status_code)
print('redirect_chain:', resp.redirect_chain)
print('template_names:', getattr(resp, 'templates', None) and [t.name for t in resp.templates])
print('content snippet:', resp.content[:500].decode('utf-8', errors='replace'))
