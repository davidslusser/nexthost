"""
Views used specifically for handling AJAX Requests on Amazon objects
"""
# import system modules
import json

# import django modules
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_GET


# import models
from auditlog.models import LogEntry
from hostmgr.models import (Owner, Project, HostnamePattern, Hostname)


@require_GET
def get_owner_details(request):
    """
    Description:
        Get details for a given Owner.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            object_id = request.GET['client_response']
            obj = Owner.objects.get(id=object_id)
            queryset = obj.jiras.all()
            template = loader.get_template('ajax/get_owner_details.htm')
            return HttpResponse(json.dumps({"server_response": template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse("Invalid request inputs", status=400)
    else:
        return HttpResponse("Invalid request", status=400)


@require_GET
def get_project_details(request):
    """
    Description:
        Get details for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            object_id = request.GET['client_response']
            obj = Project.objects.get(id=object_id)
            template = loader.get_template('ajax/get_project_details.htm')
            return HttpResponse(json.dumps({"server_response": template.render({'object': obj})}),
                                content_type='application/javascript')
        else:
            return HttpResponse("Invalid request inputs", status=400)
    else:
        return HttpResponse("Invalid request", status=400)


@require_GET
def get_pattern_details(request):
    """
    Description:
        Get details for a given HostnamePattern.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            object_id = request.GET['client_response']
            obj = HostnamePattern.objects.get(id=object_id)
            template = loader.get_template('ajax/get_pattern_details.htm')
            return HttpResponse(json.dumps({"server_response": template.render({'object': obj})}),
                                content_type='application/javascript')
        else:
            return HttpResponse("Invalid request inputs", status=400)
    else:
        return HttpResponse("Invalid request", status=400)


@require_GET
def get_hostname_details(request):
    """
    Description:
        Get details for a given Hostname.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            object_id = request.GET['client_response']
            obj = Hostname.objects.get(id=object_id)
            template = loader.get_template('ajax/get_hostname_details.htm')
            return HttpResponse(json.dumps({"server_response": template.render({'queryset': obj})}),
                                content_type='application/javascript')
        else:
            return HttpResponse("Invalid request inputs", status=400)
    else:
        return HttpResponse("Invalid request", status=400)
