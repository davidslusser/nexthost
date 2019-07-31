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
from hostmgr.models import (Owner, Project, HostnamePattern, AssetIdType, Hostname)


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
    queryset = Project.objects.all().select_related('owner').prefetch_related('hostnamepattern_set')
    title = "Projects"
    page_description = ""
    table = "table/table_projects.htm"


class ListPatterns(HostmgrBaseListView):
    """ list available HostnamePattern entries """
    queryset = HostnamePattern.objects.all().select_related('project').prefetch_related('hostname_set')
    title = "Hostname Patterns"
    page_description = ""
    table = "table/table_patterns.htm"
