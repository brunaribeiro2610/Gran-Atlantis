import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','setup.settings')
import django
django.setup()
from django.test import Client
c = Client()
resp = c.get('/accounts/logout/')
print('status_code:', resp.status_code)
print('has_redirect_chain:', hasattr(resp, 'redirect_chain'))
print('redirect_chain:', getattr(resp, 'redirect_chain', None))
print('template_names:', [t.name for t in getattr(resp, 'templates', []) if hasattr(t,'name')])
print('content snippet:', getattr(resp, 'content', b'')[:500].decode('utf-8', errors='replace'))
