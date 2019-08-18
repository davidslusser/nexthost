from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import (View, ListView, DetailView, TemplateView)
from djangohelpers.views import FilterByQueryParamsMixin
from rest_framework.authtoken.models import Token
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, Sum
import datetime

# import models
from hostmgr.models import (Owner, Project, Pattern, AssetIdType, Hostname)


class HostmgrBaseListView(FilterByQueryParamsMixin, ListView):
    """ base view for hostmgr list pages """
    title = None
    table = None

    def get(self, request, *args, **kwargs):
        context = dict()
        template = "generic/generic_list.html"
        context['queryset'] = self.filter_by_query_params()
        context['title'] = self.title
        context['sub_title'] = self.page_description
        context['table'] = self.table
        return render(request, template, context=context)


class ListOwners(HostmgrBaseListView):
    """ list available Owner entries """
    queryset = Owner.objects.all().select_related('group').prefetch_related('project_set').order_by('-created_at')
    title = "Owners"
    page_description = ""
    table = "table/table_owners.htm"


class ListProjects(HostmgrBaseListView):
    """ list available Project entries """
    queryset = Project.objects.all().select_related('owner').prefetch_related('pattern_set')
    title = "Projects"
    page_description = ""
    table = "table/table_projects.htm"


class ListPatterns(HostmgrBaseListView):
    """ list available Pattern entries """
    queryset = Pattern.objects.all().select_related('project').prefetch_related('hostname_set')
    title = "Patterns"
    page_description = ""
    table = "table/table_patterns.htm"


class ListHostnames(HostmgrBaseListView):
    """ list available Hostname entries """
    queryset = Hostname.objects.all().select_related('pattern', 'pattern__project', 'pattern__project__owner'
                                                     ).order_by('hostname')
    title = "Hostnames"
    page_description = ""
    table = "table/table_hosts.htm"


class DetailOwner(DetailView):
    """ display details of a specific owner """
    model = Owner
    template_name = "detail/detail_owner.html"


class DetailProject(DetailView):
    """ display details of a specific project """
    model = Project
    template_name = "detail/detail_project.html"


class DetailPattern(DetailView):
    """ display details of a specific pattern """
    model = Pattern
    template_name = "detail/detail_pattern.html"
    queryset = model.objects.all().select_related('project__owner')


class ShowAdminPanel(LoginRequiredMixin, View):
    """ display actions only provided to admins """
    def get(self, request, *args, **kwargs):
        template = "custom/admin_panel.html"
        context = dict()
        return render(request, template, context=context)


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
            messages.add_message(request, messages.INFO, "{} set to 'assigned'".format(hostname.hostname),
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
            messages.add_message(request, messages.INFO, "assignment on {} has been released".format(hostname.hostname),
                                 extra_tags='alert-success')
        except Exception as err:
            messages.add_message(request, messages.ERROR, err, extra_tags='alert-danger')
        return redirect(redirect_url)
