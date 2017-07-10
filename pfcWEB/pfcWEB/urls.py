"""makeDashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from social_django.urls import urlpatterns as social_django_urls
from creador import views


urlpatterns = [
    url(r'^creador/', include('creador.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^tareas/', include('creador.urls', namespace="utareas")),
    url(r'^oauth/complete/github/', views.indexregistrado, name="pantallainicio" ),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    #url(r'^oauth/complete/github/', views.indexregistrado ),
]
