from django.views.generic import (View, ListView, TemplateView, DeleteView)
from django.shortcuts import render, redirect
from django.contrib import messages
from djangohelpers.views import FilterByQueryParamsMixin
from rest_framework.authtoken.models import Token
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


# import models
from userextensions.models import (UserRecent, UserFavorite)
from hostmgr.models import (Owner, Project, Pattern, Hostname)


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='PadLock APIs')
    return response.Response(generator.get_schema(request=request))


class ShowUserProfile(LoginRequiredMixin, View):
    """ show user profile """
    @staticmethod
    def get(request):
        context = dict()
        context['user'] = request.user
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        context['groups'] = sorted([i.name for i in request.user.groups.all()])
        return render(request, "detail/detail_current_user.html", context)


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


class ShowDashboard(LoginRequiredMixin, View):
    """ display project-level dashboard that includes: total count of projects, hostname patterns, hostnames,
    break down of hostname usage (available, assigned, reserved, expired) and 24hr activity """
    def get(self, request, *args, **kwargs):
        template = "custom/nexthost_dashboard.html"
        context = dict()
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
        return render(request, template, context=context)
