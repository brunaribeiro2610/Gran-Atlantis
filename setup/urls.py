"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Verifique se o 'include' está importado
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    # Verifique se está EXATAMENTE assim:
    path('', include('core.urls', namespace='core')), 
    

    
    # Sistema de login padrão do Django
    path('accounts/', include('django.contrib.auth.urls')), 
]

# Configuração para carregar as imagens (QR Code e Logo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)