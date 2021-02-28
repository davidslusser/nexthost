from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.utils import timezone
from django.views.generic import (View, ListView, DetailView, TemplateView)
from handyhelpers.views import (HandyHelperIndexView, HandyHelperListView, HandyHelperListPlusCreateView,
                                HandyHelperListPlusFilterView, HandyHelperListPlusCreateAndFilterView)
from rest_framework.authtoken.models import Token
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, Sum
import datetime

# import models
from hostmgr.models import (Owner, Project, Pattern, AssetIdType, Hostname)

# import forms
from hostmgr.forms import (OwnerForm, ProjectForm, PatternForm,
                           FilterOwnerForm, FilterProjectForm, FilterPatternForm, FilterHostnameForm)

from hostmgr.helpers.queryset_helpers import get_hr_trend_data, get_hr_trend_labels


class IndexHostmgr(HandyHelperIndexView):
    title = 'Welcome to <span class="text-primary">Next</span><span class="text-secondary">Host</span>!'
    subtitle = 'Select an option below to get started'
    item_list = [
        {
            'url': '/hostmgr/show_dashboard',
            'icon': 'fas fa-chart-line',
            'title': 'Dashboard',
            'description': 'View counts, stats, and trends',
        },
        {
            'url': '/hostmgr/list_owners',
            'icon': 'fas fa-users',
            'title': 'Owners',
            'description': 'List all owners',
        },
        {
            'url': '/hostmgr/list_projects',
            'icon': 'fas fa-project-diagram',
            'title': 'Projects',
            'description': 'List all projects',
        },
        {
            'url': '/hostmgr/list_patterns',
            'icon': 'fas fa-swatchbook',
            'title': 'Patterns',
            'description': 'List all patterns',
        },
        {
            'url': '/hostmgr/list_hostnames',
            'icon': 'fas fa-server',
            'title': 'Hostnames',
            'description': 'List all hostnames',
        },
    ]
    protected_item_list = [
        {
            'url': '/hostmgr/show_admin_panel',
            'icon': 'fas fa-id-card-alt',
            'title': 'Admin Panel',
            'description': 'Manage owners, projects, and patterns',
        },
        {
            'url': '/admin',
            'icon': 'fab fa-python',
            'title': 'Django Console',
            'description': 'Access the django administrator console',
        },
    ]
    protected_group_name = 'admins'


class ListOwners(HandyHelperListPlusCreateAndFilterView):
    """ list available Owner entries """
    queryset = Owner.objects.all().select_related('group').prefetch_related('project_set').order_by('-created_at')
    title = 'Owners'
    page_description = ''
    table = 'hostmgr/table/table_owners.htm'

    create_form_obj = OwnerForm
    create_form_url = '/hostmgr/create_owner/'
    create_form_title = '<b>Add Owner: </b><small> </small>'
    create_form_modal = 'add_owner'
    create_form_tool_tip = 'add a new owner'

    filter_form_obj = FilterOwnerForm
    filter_form_title = '<b>Filter Owners: </b><small> </small>'
    filter_form_modal = 'filter_owners'
    filter_form_tool_tip = 'filter patterns'


class ListProjects(HandyHelperListPlusCreateAndFilterView):
    """ list available Project entries """
    queryset = Project.objects.all().select_related('owner').prefetch_related('pattern_set')
    title = 'Projects'
    page_description = ''
    table = 'hostmgr/table/table_projects.htm'

    create_form_obj = ProjectForm
    create_form_url = '/hostmgr/create_project/'
    create_form_title = '<b>Add Project: </b><small> </small>'
    create_form_modal = 'add_project'
    create_form_tool_tip = 'add a new project'

    filter_form_obj = FilterProjectForm
    filter_form_title = '<b>Filter Projects: </b><small> </small>'
    filter_form_modal = 'filter_projects'
    filter_form_tool_tip = 'filter patterns'


class ListPatterns(HandyHelperListPlusCreateAndFilterView):
    """ list available Pattern entries """
    queryset = Pattern.objects.all().select_related('project').prefetch_related('hostname_set')
    title = 'Patterns'
    page_description = ''
    table = 'hostmgr/table/table_patterns.htm'

    create_form_obj = PatternForm
    create_form_url = '/hostmgr/create_pattern/'
    create_form_title = '<b>Add Pattern: </b><small> </small>'
    create_form_modal = 'add_pattern'
    create_form_tool_tip = 'add a new pattern'

    filter_form_obj = FilterPatternForm
    filter_form_title = '<b>Filter Patterns: </b><small> </small>'
    filter_form_modal = 'filter_patterns'
    filter_form_tool_tip = 'filter patterns'


class ListHostnames(HandyHelperListPlusFilterView):
    """ list available Hostname entries """
    queryset = Hostname.objects.all().select_related('pattern', 'pattern__project', 'pattern__project__owner'
                                                     ).order_by('hostname')
    title = 'Hostnames'
    page_description = ''
    table = 'hostmgr/table/table_hostnames.htm'
    modals = 'hostmgr/forms/form_assign_hostname.htm'

    filter_form_obj = FilterHostnameForm
    filter_form_title = '<b>Filter Hostnames: </b><small> </small>'
    filter_form_modal = 'filter_hostnames'
    filter_form_tool_tip = 'filter hostnames'


class DetailOwner(DetailView):
    """ display details of a specific owner """
    model = Owner
    template_name = 'hostmgr/detail/detail_owner.html'


class DetailProject(DetailView):
    """ display details of a specific project """
    model = Project
    template_name = 'hostmgr/detail/detail_project.html'

    def get_context_data(self, **kwargs):
        context = super(DetailProject, self).get_context_data(**kwargs)
        context['hostnames_assigned'] = get_hr_trend_data(self.object.get_assigned_hostnames(), 12, 'updated_at')
        context['hostnames_reserved'] = get_hr_trend_data(self.object.get_reserved_hostnames(), 12, 'updated_at')
        context['hostnames_available'] = get_hr_trend_data(self.object.get_available_hostnames(), 12, 'updated_at')
        context['hostnames_expired'] = get_hr_trend_data(self.object.get_expired_hostnames(), 12, 'updated_at')

        # include pattern form
        form_add_pattern = dict()
        form_add_pattern['form'] = PatternForm(self.request.POST or None, {'project': self.object},
                                               initial={'project': self.object})
        form_add_pattern['action'] = 'Add'
        # form_add_pattern['action_url'] = reverse('hostmgr:show_admin_panel') + "?action=add_pattern"
        form_add_pattern['action_url'] = reverse('hostmgr:create_pattern')
        form_add_pattern['title'] = '<b>Add Pattern: </b><small> </small>'
        form_add_pattern['modal_name'] = 'add_pattern'
        context['form_add_pattern'] = form_add_pattern

        return context


class DetailPattern(DetailView):
    """ display details of a specific pattern """
    model = Pattern
    template_name = 'hostmgr/detail/detail_pattern.html'
    queryset = model.objects.all().select_related('project__owner')


class ShowDashboard(LoginRequiredMixin, View):
    """ display project-level dashboard that includes: total count of projects, hostname patterns, hostnames,
    break down of hostname usage (available, assigned, reserved, expired) and 12hr activity """
    def get(self, request, *args, **kwargs):
        template = 'hostmgr/custom/hostmgr_dashboard.html'
        context = dict()
        now = timezone.now()
        context['projects'] = Project.objects.all()
        context['patterns'] = Pattern.objects.all()
        context['owners'] = Owner.objects.all()
        hostnames = Hostname.objects.all()
        context['hostnames_all'] = hostnames
        context['hostnames_available'] = hostnames.filter(status='available')
        context['hostnames_assigned'] = hostnames.filter(status='assigned')
        context['hostnames_reserved'] = hostnames.filter(status='reserved')
        context['hostnames_expired'] = hostnames.filter(status='expired')
        context['activity'] = None
        context['trend_hostnames_assigned'] = get_hr_trend_data(hostnames.filter(status='assigned'), 12,
                                                                'updated_at', now=now)
        context['trend_hostnames_reserved'] = get_hr_trend_data(hostnames.filter(status='reserved'), 12,
                                                                'updated_at', now=now)
        context['trend_hostnames_available'] = get_hr_trend_data(hostnames.filter(status='available'), 12,
                                                                 'updated_at', now=now)
        context['trend_hostnames_expired'] = get_hr_trend_data(hostnames.filter(assignment_expires__lte=timezone.now()),
                                                               12, 'updated_at', now=now)
        context['hour_labels'] = get_hr_trend_labels(hrs=12, now=now)
        return render(request, template, context=context)


class ShowAdminPanel(LoginRequiredMixin, View):
    """ display actions only provided to admins """
    def add_owner(self, redirect_url):
        """ add an owner """
        form = OwnerForm(self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, f'Owner \'{new_record}\' created!',
                                 extra_tags='alert-info', )
            return redirect(redirect_url)
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, f'Input error: {error}',
                                     extra_tags='alert-danger', )
            return self.get(self.request)

    def add_project(self, redirect_url):
        """ add a project """
        form = ProjectForm(self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, f'Project \'{new_record}\' created!',
                                 extra_tags='alert-info', )
            return redirect(redirect_url)
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, f'Input error: {error}',
                                     extra_tags='alert-danger', )
            return self.get(self.request)

    def add_pattern(self, redirect_url):
        """ add a pattern """
        form = PatternForm(self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, f'Pattern \'{new_record}\' created!',
                                 extra_tags='alert-info', )
            return redirect(redirect_url)
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, f'Input error: {error}',
                                     extra_tags='alert-danger', )
            return self.get(self.request)

    def get(self, request, *args, **kwargs):
        template = 'hostmgr/custom/admin_panel.html'
        context = dict()

        # include owner form
        form_add_owner = dict()
        form_add_owner['form'] = OwnerForm(request.POST or None)
        form_add_owner['action'] = 'Add'
        form_add_owner['action_url'] = reverse('hostmgr:show_admin_panel') + '?action=add_owner'
        form_add_owner['title'] = '<b>Add Owner: </b><small> </small>'
        form_add_owner['modal_name'] = 'add_owner'
        context['form_add_owner'] = form_add_owner

        # include project form
        form_add_project = dict()
        form_add_project['form'] = ProjectForm(request.POST or None)
        form_add_project['action'] = 'Add'
        form_add_project['action_url'] = reverse('hostmgr:show_admin_panel') + '?action=add_project'
        form_add_project['title'] = '<b>Add Project: </b><small> </small>'
        form_add_project['modal_name'] = 'add_project'
        context['form_add_project'] = form_add_project

        # include pattern form
        form_add_pattern = dict()
        form_add_pattern['form'] = PatternForm(request.POST or None)
        form_add_pattern['action'] = 'Add'
        form_add_pattern['action_url'] = reverse('hostmgr:show_admin_panel') + '?action=add_patterm'
        form_add_pattern['title'] = '<b>Add Pattern: </b><small> </small>'
        form_add_pattern['modal_name'] = 'add_pattern'
        context['form_add_pattern'] = form_add_pattern

        return render(request, template, context=context)

    def post(self, request):
        redirect_url = self.request.META.get('HTTP_REFERER')
        action = self.request.GET.dict().get('action', None)

        if action in ['add_owner']:
            return self.add_owner(redirect_url)
        elif action in ['add_project']:
            return self.add_project(redirect_url)
        elif action in ['add_pattern']:
            return self.add_pattern(redirect_url)
        else:
            print('FAILED!')
            messages.add_message(request, messages.ERROR, 'Could not complete requested action',
                                 extra_tags='alert-danger')
            return self.get(request)


class ShowApiGuideIndex(LoginRequiredMixin, View):
    """ display index page for api help docs """
    @staticmethod
    def get(request):
        template = 'custom/api_guide_index.html'
        context = dict()
        context['title'] = 'API Guide'
        context['sub_title'] = 'Hostname endpoints'
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)


class ShowApiGuideV1Owner(LoginRequiredMixin, View):
    """ display api documentation for Owner apis (v1) """
    @staticmethod
    def get(request):
        template = 'custom/api_guide_v1_owner.html'
        context = dict()
        context['title'] = 'Owner APIs'
        context['sub_title'] = 'v1'
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)


class ShowApiGuideV1Project(LoginRequiredMixin, View):
    """ display api documentation for Project apis (v1) """
    @staticmethod
    def get(request):
        template = 'custom/api_guide_v1_project.html'
        context = dict()
        context['title'] = 'Project APIs'
        context['sub_title'] = 'v1'
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)


class ShowApiGuideV1Pattern(LoginRequiredMixin, View):
    """ display api documentation for Pattern apis (v1) """
    @staticmethod
    def get(request):
        template = 'custom/api_guide_v1_pattern.html'
        context = dict()
        context['title'] = 'Pattern APIs'
        context['sub_title'] = 'v1'
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)


class ShowApiGuideV1Hostname(LoginRequiredMixin, View):
    """ display api documentation for Hostname apis (v1) """
    @staticmethod
    def get(request):
        template = 'custom/api_guide_v1_hostname.html'
        context = dict()
        context['title'] = 'Hostname APIs'
        context['sub_title'] = 'v1'
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)
