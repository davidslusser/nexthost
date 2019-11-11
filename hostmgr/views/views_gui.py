from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views.generic import (View, ListView, DetailView, TemplateView)
from djangohelpers.views import FilterByQueryParamsMixin
from rest_framework.authtoken.models import Token
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count, Sum
import datetime

# import models
from django.contrib.auth.models import Group, Permission, User
from hostmgr.models import (Owner, Project, Pattern, AssetIdType, Hostname)

# import forms
from hostmgr.forms import (OwnerForm, ProjectForm, PatternForm)


class HostmgrBaseListView(FilterByQueryParamsMixin, ListView):
    """ base view for hostmgr list pages """
    title = None
    table = None
    modals = None

    def get(self, request, *args, **kwargs):
        context = dict()
        template = "generic/generic_list.html"
        context['queryset'] = self.filter_by_query_params()
        context['title'] = self.title
        context['sub_title'] = self.page_description
        context['table'] = self.table
        context['modals'] = self.modals
        return render(request, template, context=context)


class HostMgrBaseListViewCreate(FilterByQueryParamsMixin, ListView):
    """ base view for hostmgr list pages that include create forms """
    title = None
    table = None
    modals = None
    create_form = dict()
    create_form_obj = None
    create_form_url = None
    create_form_title = None
    create_form_modal = None
    create_form_link_title = None

    def get(self, request, *args, **kwargs):
        context = dict()
        template = "generic/generic_list.html"
        context['queryset'] = self.filter_by_query_params()
        context['title'] = self.title
        context['sub_title'] = self.page_description
        context['table'] = self.table
        context['modals'] = self.modals
        if self.create_form_obj:
            self.create_form['form'] = self.create_form_obj
            self.create_form['form'] = self.create_form_obj(request.user.username, request.POST or None)
            self.create_form['action'] = "Add"
            self.create_form['action_url'] = self.create_form_url
            self.create_form['title'] = self.create_form_title
            self.create_form['modal_name'] = self.create_form_modal
            self.create_form['link_title'] = self.create_form_link_title
            context['create_form'] = self.create_form
        return render(request, template, context=context)


class ListOwners(HostMgrBaseListViewCreate):
    """ list available Owner entries """
    queryset = Owner.objects.all().select_related('group').prefetch_related('project_set').order_by('-created_at')
    title = "Owners"
    page_description = ""
    table = "table/table_owners.htm"
    create_form_obj = OwnerForm
    create_form_url = '/hostmgr/create_owner/'
    create_form_title = "<b>Add Owner: </b><small> </small>"
    create_form_modal = "add_owner"
    create_form_link_title = "add owner"


class ListProjects(HostMgrBaseListViewCreate):
    """ list available Project entries """
    queryset = Project.objects.all().select_related('owner').prefetch_related('pattern_set')
    title = "Projects"
    page_description = ""
    table = "table/table_projects.htm"
    create_form_obj = ProjectForm
    create_form_url = '/hostmgr/create_project/'
    create_form_title = "<b>Add Project: </b><small> </small>"
    create_form_modal = "add_project"
    create_form_link_title = "add project"


class ListPatterns(HostMgrBaseListViewCreate):
    """ list available Pattern entries """
    queryset = Pattern.objects.all().select_related('project').prefetch_related('hostname_set')
    title = "Patterns"
    page_description = ""
    table = "table/table_patterns.htm"
    create_form_obj = PatternForm
    create_form_url = '/hostmgr/create_pattern/'
    create_form_title = "<b>Add Pattern: </b><small> </small>"
    create_form_modal = "add_pattern"
    create_form_link_title = "add pattern"


class ListHostnames(HostmgrBaseListView):
    """ list available Hostname entries """
    queryset = Hostname.objects.all().select_related('pattern', 'pattern__project', 'pattern__project__owner'
                                                     ).order_by('hostname')
    title = "Hostnames"
    page_description = ""
    table = "table/table_hostnames.htm"
    modals = "forms/hostmgr_modals_test.htm"


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
    def add_owner(self, redirect_url):
        """ add an owner """
        form = OwnerForm(self.request.POST or None)
        if form.is_valid():
            print("valid...")
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, "Owner '{}' created!".format(new_record),
                                 extra_tags='alert-info', )
            return redirect(redirect_url)
        else:
            for error in form.errors:
                print("GOT AN ERROR...")
                messages.add_message(self.request, messages.ERROR, "Input error: {}".format(error),
                                     extra_tags='alert-danger', )
            return self.get(self.request)

    def add_project(self, redirect_url):
        """ add a project """
        form = ProjectForm(self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, "Project '{}' created!".format(new_record),
                                 extra_tags='alert-info', )
            return redirect(redirect_url)
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, "Input error: {}".format(error),
                                     extra_tags='alert-danger', )
            return self.get(self.request)

    def add_pattern(self, redirect_url):
        """ add a pattern """
        form = PatternForm(self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, "Pattern '{}' created!".format(new_record),
                                 extra_tags='alert-info', )
            return redirect(redirect_url)
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, "Input error: {}".format(error),
                                     extra_tags='alert-danger', )
            return self.get(self.request)

    def get(self, request, *args, **kwargs):
        template = "custom/admin_panel.html"
        context = dict()

        # include owner form
        form_add_owner = dict()
        form_add_owner['form'] = OwnerForm(request.POST or None)
        form_add_owner['action'] = "Add"
        form_add_owner['action_url'] = reverse('hostmgr:show_admin_panel') + "?action=add_owner"
        form_add_owner['title'] = "<b>Add Owner: </b><small> </small>"
        form_add_owner['modal_name'] = "add_owner"
        context['form_add_owner'] = form_add_owner

        # include project form
        form_add_project = dict()
        form_add_project['form'] = ProjectForm(request.POST or None)
        form_add_project['action'] = "Add"
        form_add_project['action_url'] = reverse('hostmgr:show_admin_panel') + "?action=add_project"
        form_add_project['title'] = "<b>Add Project: </b><small> </small>"
        form_add_project['modal_name'] = "add_project"
        context['form_add_project'] = form_add_project

        # include pattern form
        form_add_pattern = dict()
        form_add_pattern['form'] = PatternForm(request.POST or None)
        form_add_pattern['action'] = "Add"
        form_add_pattern['action_url'] = reverse('hostmgr:show_admin_panel') + "?action=add_patterm"
        form_add_pattern['title'] = "<b>Add Pattern: </b><small> </small>"
        form_add_pattern['modal_name'] = "add_pattern"
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
            print("FAILED!")
            messages.add_message(request, messages.ERROR, "Could not complete requested action",
                                 extra_tags='alert-danger')
            return self.get(request)


class ShowApiGuideIndex(LoginRequiredMixin, View):
    """ display index page for api help docs """
    @staticmethod
    def get(request):
        template = "custom/api_guide_index.html"
        context = dict()
        context['title'] = 'API Guide'
        context['sub_title'] = "Hostname endpoints"
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)


class ShowApiGuideV1Owner(LoginRequiredMixin, View):
    """ display api documentation for Owner apis (v1) """
    @staticmethod
    def get(request):
        template = "custom/api_guide_v1_owner.html"
        context = dict()
        context['title'] = 'Owner APIs'
        context['sub_title'] = "v1"
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)


class ShowApiGuideV1Project(LoginRequiredMixin, View):
    """ display api documentation for Project apis (v1) """
    @staticmethod
    def get(request):
        template = "custom/api_guide_v1_project.html"
        context = dict()
        context['title'] = 'Project APIs'
        context['sub_title'] = "v1"
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)


class ShowApiGuideV1Pattern(LoginRequiredMixin, View):
    """ display api documentation for Pattern apis (v1) """
    @staticmethod
    def get(request):
        template = "custom/api_guide_v1_pattern.html"
        context = dict()
        context['title'] = 'Pattern APIs'
        context['sub_title'] = "v1"
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        return render(request, template, context=context)


class ShowApiGuideV1Hostname(LoginRequiredMixin, View):
    """ display api documentation for Hostname apis (v1) """
    @staticmethod
    def get(request):
        template = "custom/api_guide_v1_hostname.html"
        context = dict()
        context['title'] = 'Hostname APIs'
        context['sub_title'] = "v1"
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
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


class CreateOwner(LoginRequiredMixin, View):
    """ """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        redirect_url = self.request.META.get('HTTP_REFERER')
        form = OwnerForm(request.user.username, self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, "Owner '{}' created!".format(new_record),
                                 extra_tags='alert-info', )
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, "Input error: {}".format(error),
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
            messages.add_message(self.request, messages.INFO, "Project '{}' created!".format(new_record),
                                 extra_tags='alert-info', )
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, "Input error: {}".format(error),
                                     extra_tags='alert-danger', )
        return redirect(redirect_url)


class CreatePattern(LoginRequiredMixin, View):
    """ """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        redirect_url = self.request.META.get('HTTP_REFERER')
        form = PatternForm(request.user.username, self.request.POST or None)
        if form.is_valid():
            new_record = form.cleaned_data['name']
            form.save()
            messages.add_message(self.request, messages.INFO, "Pattern '{}' created!".format(new_record),
                                 extra_tags='alert-info', )
        else:
            for error in form.errors:
                messages.add_message(self.request, messages.ERROR, "Input error: {}".format(error),
                                     extra_tags='alert-danger', )
        return redirect(redirect_url)
