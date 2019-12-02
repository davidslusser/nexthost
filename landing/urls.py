from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView

# import views


app_name = 'landing'


urlpatterns = [
    # custom views
    path('', TemplateView.as_view(template_name='landing.html'), name=""),
    path('', TemplateView.as_view(template_name='landing.html'), name="home"),
    path('', TemplateView.as_view(template_name='landing.html'), name="index"),

]
