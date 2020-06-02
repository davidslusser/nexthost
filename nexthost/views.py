"""
Description: this file provides project-level views
"""

from django.views.generic import (View, ListView, UpdateView)
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.utils import timezone
from djangohelpers.views import FilterByQueryParamsMixin
from rest_framework.authtoken.models import Token
from braces.views import LoginRequiredMixin
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# import models
from hostmgr.models import (Owner, Project, Pattern, Hostname)


from hostmgr.helpers.queryset_helpers import get_hr_trend_data, get_hr_trend_labels



@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='NextHost APIs')
    return response.Response(generator.get_schema(request=request))


class RegisterUser(generic.CreateView):
    """ add a new user to NextHost """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register_user.html'


class ShowDashboard(LoginRequiredMixin, View):
    """ display project-level dashboard that includes: total count of projects, hostname patterns, hostnames,
    break down of hostname usage (available, assigned, reserved, expired) and 24hr activity """
    def get(self, request, *args, **kwargs):
        template = "custom/nexthost_dashboard.html"
        context = dict()
        now = timezone.now()
        context['projects'] = Project.objects.all()
        context['patterns'] = Pattern.objects.all()
        context['owners'] = Owner.objects.all()
        hostnames = Hostname.objects.all()
        context['hostnames_all'] = hostnames
        context['hostnames_available'] = hostnames.filter(status="available")
        context['hostnames_assigned'] = hostnames.filter(status="assigned")
        context['hostnames_reserved'] = hostnames.filter(status="reserved")
        context['hostnames_expired'] = hostnames.filter(status="expired")
        context['activity'] = None
        context['trend_hostnames_assigned'] = get_hr_trend_data(hostnames.filter(status='assigned'), 12, 'updated_at', now=now)
        context['trend_hostnames_reserved'] = get_hr_trend_data(hostnames.filter(status='reserved'), 12, 'updated_at', now=now)
        context['trend_hostnames_available'] = get_hr_trend_data(hostnames.filter(status='available'), 12, 'updated_at', now=now)
        context['trend_hostnames_expired'] = get_hr_trend_data(hostnames.filter(assignment_expires__lte=timezone.now()), 12, 'updated_at', now=now)
        context['hour_labels'] = get_hr_trend_labels(hrs=12, now=now)
        return render(request, template, context=context)
