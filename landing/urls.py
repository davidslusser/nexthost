from django.urls import path
from django.views.generic import TemplateView

app_name = 'landing'


urlpatterns = [
    # custom views
    path('', TemplateView.as_view(template_name='landing/landing.html'), name=''),
    path('', TemplateView.as_view(template_name='landing/landing.html'), name='home'),
    path('', TemplateView.as_view(template_name='landing/landing.html'), name='index'),
]
