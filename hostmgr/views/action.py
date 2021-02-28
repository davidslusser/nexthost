"""
This file contains view that perform an action and are redirected to another URL. These view do not render a template.
"""

from django.shortcuts import redirect
from django.views.generic import (View)
from braces.views import LoginRequiredMixin
from django.contrib import messages

# import models
from hostmgr.models import (Hostname)

# import forms
from hostmgr.forms import (OwnerForm, ProjectForm, PatternForm)


class ReserveHostname(LoginRequiredMixin, View):
    """ request reservation of a hostname """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        redirect_url = self.request.META.get('HTTP_REFERER')
        obj_id = self.request.GET.dict().get('id', None)
        hostname = Hostname.objects.get_object_or_none(id=obj_id)
        try:
            hostname.reserve_hostname(user=request.user)
        except Exception as err:
            messages.add_message(request, messages.ERROR, err, extra_tags='alert-danger')
        return redirect(redirect_url)


class AssignHostname(LoginRequiredMixin, View):
    """ assign reservation of a hostname """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        redirect_url = self.request.META.get('HTTP_REFERER')
        obj_id = self.request.GET.dict().get('id', None)
        asset_id = self.request.GET.dict().get('asset_id', None)
        asset_id_type_name = self.request.GET.dict().get('asset_id_type', None)
        persistent = self.request.GET.dict().get('persistent', None)

        hostname = Hostname.objects.get_object_or_none(id=obj_id)
        try:
            hostname.assign_hostname(user=request.user, asset_id=asset_id,
                                     asset_id_type_name=asset_id_type_name, persistent=persistent)
            messages.add_message(request, messages.INFO, f'{hostname.hostname} set to \'assigned\'',
                                 extra_tags='alert-success')
        except Exception as err:
            messages.add_message(request, messages.ERROR, err, extra_tags='alert-danger')
        return redirect(redirect_url)


class ReleaseHostname(LoginRequiredMixin, View):
    """ release reservation of a hostname """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        redirect_url = self.request.META.get('HTTP_REFERER')
        obj_id = self.request.GET.dict().get('id', None)
        hostname = Hostname.objects.get_object_or_none(id=obj_id)
        try:
            hostname.release_hostname(user=request.user)
            messages.add_message(request, messages.INFO, f'assignment on {hostname.hostname} has been released',
                                 extra_tags='alert-success')
        except Exception as err:
            messages.add_message(request, messages.ERROR, err, extra_tags='alert-danger')
        return redirect(redirect_url)


class CreateOwner(LoginRequiredMixin, View):
    """ """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        redirect_url = self.request.META.get('HTTP_REFERER')
        form = OwnerForm(request.user.username, self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, f'Owner \'{new_record}\' created!',
                                 extra_tags='alert-info', )
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, f'Input error: {error}',
                                     extra_tags='alert-danger', )
        return redirect(redirect_url)


class CreateProject(LoginRequiredMixin, View):
    """ """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        redirect_url = self.request.META.get('HTTP_REFERER')
        form = ProjectForm(request.user.username, self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, f'Project \'{new_record}\' created!',
                                 extra_tags='alert-info', )
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, f'Input error: {error}',
                                     extra_tags='alert-danger', )
        return redirect(redirect_url)


class CreatePattern(LoginRequiredMixin, View):
    """ """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        redirect_url = self.request.META.get('HTTP_REFERER')
        form = PatternForm(request.user.username, None, self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, f'Pattern \'{new_record}\' created!',
                                 extra_tags='alert-info', )
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, f'Input error: {error}',
                                     extra_tags='alert-danger', )
        return redirect(redirect_url)
