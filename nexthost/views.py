from django.views.generic import (View, ListView, TemplateView, DeleteView)
from django.shortcuts import render, redirect
from djangohelpers.views import FilterByQueryParamsMixin
from rest_framework.authtoken.models import Token
from braces.views import LoginRequiredMixin, GroupRequiredMixin


# import models
from userextensions.models import (UserRecent, UserFavorite)


class ShowUserProfile(LoginRequiredMixin, View):
    """ show user profile """
    @staticmethod
    def get(request):
        context = dict()
        context['user'] = request.user
        context['token'] = str(Token.objects.get_or_create(user=request.user)[0])
        context['groups'] = sorted([i.name for i in request.user.groups.all()])
        context['pclouds'] = []
        return render(request, "detail/detail_current_user.html", context)


class ListRecents(LoginRequiredMixin, FilterByQueryParamsMixin, ListView):
    """  """
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
    """ """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = UserFavorite.objects.filter(user=request.user).order_by('-updated_at')
        template = "generic/generic_list.html"
        context['queryset'] = self.filter_by_query_params()
        context['title'] = "Favorites"
        context['sub_title'] = request.user.username
        context['table'] = "table/table_favorites.htm"
        return render(request, template, context=context)
