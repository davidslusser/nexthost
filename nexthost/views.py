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
from userextensions.models import (UserRecent, UserFavorite, UserPreference)
from hostmgr.models import (Owner, Project, Pattern, Hostname)

# import forms
from nexthost.forms import (UserPreferenceForm)

from hostmgr.helpers.queryset_helpers import get_hr_trend_data, get_hr_trend_labels



@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='PadLock APIs')
    return response.Response(generator.get_schema(request=request))


class ShowUserProfile(LoginRequiredMixin, View):
    """ show user profile """
    template = "detail/detail_current_user.html"

    def get(self, request):
        context = dict()

        # include user preference form
        form_data_user_preferences = dict()
        form_data_user_preferences['form'] = UserPreferenceForm(request.POST or None, instance=request.user.preference)
        form_data_user_preferences['action'] = "Update"
        form_data_user_preferences['action_url'] = reverse('detail_user')
        form_data_user_preferences['title'] = "<b>Update Preferences: </b><small> {} </small>".format(request.user)
        form_data_user_preferences['modal_name'] = "update_user_preferences"
        context['form_data_user_preferences'] = form_data_user_preferences

        context['user'] = request.user
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        context['groups'] = sorted([i.name for i in request.user.groups.all()])
        return render(request, self.template, context)

    def post(self, request):
        redirect_url = request.META.get('HTTP_REFERER')
        form = UserPreferenceForm(request.POST or None, instance=request.user.preference)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.ERROR, "Preferences updated!", extra_tags='alert-info', )
            return redirect(redirect_url)
        else:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, "Input error: {}".format(error),
                                     extra_tags='alert-danger', )
            return self.get(request)


class ListRecents(LoginRequiredMixin, FilterByQueryParamsMixin, ListView):
    """ display a list of urls the user has recently visited """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = UserRecent.objects.filter(user=request.user).order_by('-updated_at')
        template = "generic/generic_list.html"
        context['queryset'] = self.filter_by_query_params()
        context['title'] = "Recents"
        context['sub_title'] = request.user.username
        context['table'] = "table/table_recents.htm"
        return render(request, template, context=context)


class ListFavorites(LoginRequiredMixin, FilterByQueryParamsMixin, ListView):
    """ display a list of user defined favorites """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = UserFavorite.objects.filter(user=request.user).order_by('-updated_at')
        template = "generic/generic_list.html"
        context['queryset'] = self.filter_by_query_params()
        context['title'] = "Favorites"
        context['sub_title'] = request.user.username
        context['table'] = "table/table_favorites.htm"
        return render(request, template, context=context)


class UpdateApiToken(LoginRequiredMixin, View):
    """ delete current user token and create a new one """
    def post(self, request):
        redirect_url = self.request.META.get('HTTP_REFERER')
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            Token.objects.get_or_create(user=request.user)
        except Exception as err:
            messages.add_message(request, messages.ERROR, "Could not complete requested action",
                                 extra_tags='alert-danger')
        return redirect(redirect_url)


class UpdateUserPreference(LoginRequiredMixin, UpdateView):
    """ update user preferences """
    model = UserPreference
    form_class = UserPreferenceForm

    def form_valid(self, form):
        form.save()
        return super(UpdateUserPreference, self).form_valid(form)


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
