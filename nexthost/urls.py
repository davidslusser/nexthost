"""dj110 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from nexthost import views
from django.contrib.auth import urls

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('django.contrib.auth.urls')),

    # home page
    path('', TemplateView.as_view(template_name='index.html')),
    path('default', TemplateView.as_view(template_name='index.html'), name="default"),
    path('home', TemplateView.as_view(template_name='index.html'), name="home"),
    path('index', TemplateView.as_view(template_name='index.html'), name="index"),

    # project-level
    path('about', TemplateView.as_view(template_name='custom/about.html'), name="about"),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('dashboard', views.ShowDashboard.as_view(), name='dashboard'),
    path('robots.txt', TemplateView.as_view(template_name='custom/robots.txt'), name="robots"),
    path('sitemap.xml', TemplateView.as_view(template_name='custom/sitemap.xml'), name="sitemap"),
    path('test', TemplateView.as_view(template_name='custom/test.html'), name='test'),

    # app urls
    path('userextensions/', include('userextensions.urls'), ),
    path('hostmgr/', include('hostmgr.urls'), ),
    path('landing/', include('landing.urls'), ),

    # swagger API docs
    path('swagger', views.schema_view, name="swagger"),

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
