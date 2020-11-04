from django import forms

# import models
from django.contrib.auth.models import Group
from hostmgr.models import (Owner, Project, Pattern, Hostname)


class OwnerForm(forms.ModelForm):
    """ Form class used to add/edit user Owner objects """
    class Meta:
        model = Owner
        exclude = ['created_at', 'updated_at']
        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, username=None, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        if username:
            self.fields['group'].queryset = Group.objects.filter(user__username=username)


class ProjectForm(forms.ModelForm):
    """ Form class used to add/edit user Project objects """
    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at']
        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, username=None, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        if username:
            self.fields['owner'].queryset = Owner.objects.filter(group__user__username=username)


class PatternForm(forms.ModelForm):
    """ Form class used to add/edit user Pattern objects """
    class Meta:
        model = Pattern
        exclude = ['created_at', 'updated_at']
        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'prefix_delimiter': forms.TextInput(attrs={'class': 'form-control'}),
            'suffix': forms.TextInput(attrs={'class': 'form-control'}),
            'suffix_delimiter': forms.TextInput(attrs={'class': 'form-control'}),
            'host_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'increment': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_from': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, username=None, project=None, *args, **kwargs):
        super(PatternForm, self).__init__(*args, **kwargs)
        if username:
            self.fields['project'].queryset = Project.objects.filter(owner__group__user__username=username)
        if project:
            self.fields['project'].queryset = Project.objects.filter(id=project['project'].id)


class FilterOwnerForm(forms.Form):
    """ Form class used to filter Owner list view """
    def __init__(self, *args, **kwargs):
        super(FilterOwnerForm, self).__init__(*args, **kwargs)

    active = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=((True, True), (False, False)),
                               required=False)
    name__icontains = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      required=False,
                                      label='name')
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   required=False)


class FilterProjectForm(forms.Form):
    """ Form class used to filter Project list view """
    def __init__(self, *args, **kwargs):
        super(FilterProjectForm, self).__init__(*args, **kwargs)

    active = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=((True, True), (False, False)),
                               required=False)
    name__icontains = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      required=False,
                                      label='name')
    owner = forms.ModelChoiceField(queryset=Owner.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   required=False)


class FilterPatternForm(forms.Form):
    """ Form class used to filter Pattern list view """
    def __init__(self, *args, **kwargs):
        super(FilterPatternForm, self).__init__(*args, **kwargs)

    active = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=((True, True), (False, False)),
                               required=False)
    name__icontains = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      required=False,
                                      label='name')
    project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=False)
    prefix__icontains = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        required=False,
                                        label='prefix')
    suffix__icontains = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        required=False,
                                        label='suffix')
