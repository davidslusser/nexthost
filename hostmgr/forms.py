from django import forms

# import models
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
            'delimiter': forms.TextInput(attrs={'class': 'form-control'}),
            'max_hosts': forms.NumberInput(attrs={'class': 'form-control'}),
            'increment': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_from': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# class HostNameAssignForm(forms.ModelForm):
#     """ Form class used to assign a hostname to an asset """
#     class Meta:
#         model = Hostname
#         fields = ['hostname', 'asset_id_type', 'asset_id', 'is_eternal', 'assignment_expires']
#         widgets = {
#             'hostname': forms.TextInput(attrs={'class': 'form-control'}),
#             'asset_id_type': forms.Select(attrs={'class': 'form-control'}),
#             'asset_id': forms.TextInput(attrs={'class': 'form-control'}),
#             'persistent': forms.CheckboxInput(attrs={'class': 'form-control'}),
#         }

