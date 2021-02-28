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
from hostmgr.models import (Owner, Project, Pattern, Hostname)


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
            template = loader.get_template('hostmgr/ajax/get_owner_details.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


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
            template = loader.get_template('hostmgr/ajax/get_project_details.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'object': obj})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_pattern_details(request):
    """
    Description:
        Get details for a given Pattern.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            object_id = request.GET['client_response']
            obj = Pattern.objects.get(id=object_id)
            template = loader.get_template('hostmgr/ajax/get_pattern_details.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'object': obj})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


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
            template = loader.get_template('hostmgr/ajax/get_hostname_details.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'object': obj})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_hostname_auditlog(request):
    """
    Description:
        get AuditLog for a given Hostname.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            hostname = request.GET['client_response']
            queryset = LogEntry.objects.filter(content_type__model='hostname',
                                               object_repr__icontains=hostname)
            template = loader.get_template('handyhelpers/ajax/show_audit_log.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_pattern_auditlog(request):
    """
    Description:
        get AuditLog for a given Pattern.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            name = request.GET['client_response']
            queryset = LogEntry.objects.filter(content_type__model='pattern',
                                               object_repr__icontains=name)
            template = loader.get_template('hostmgr/ajax/show_audit_log.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_project_auditlog(request):
    """
    Description:
        get AuditLog for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            name = request.GET['client_response']
            queryset = LogEntry.objects.filter(content_type__model='project',
                                               object_repr__icontains=name)
            template = loader.get_template('hostmgr/ajax/show_audit_log.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_owner_auditlog(request):
    """
    Description:
        get AuditLog for a given Owner.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            name = request.GET['client_response']
            queryset = LogEntry.objects.filter(content_type__model='owner',
                                               object_repr__icontains=name)
            template = loader.get_template('hostmgr/ajax/show_audit_log.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_users_per_owner(request):
    """
    Description:
        get all users for a given Owner.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            owner_id = request.GET['client_response']
            queryset = Owner.objects.get(id=owner_id)
            template = loader.get_template('hostmgr/ajax/list_users_per_owner.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_projects_per_owner(request):
    """
    Description:
        get all projects for a given Owner.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            owner_id = request.GET['client_response']
            owner = Owner.objects.get(id=owner_id)
            queryset = owner.get_projects()
            template = loader.get_template('hostmgr/ajax/list_projects_per_owner.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_patterns_per_owner(request):
    """
    Description:
        get all patterns for a given Owner.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            owner_id = request.GET['client_response']
            owner = Owner.objects.get(id=owner_id)
            queryset = owner.get_patterns()
            template = loader.get_template('hostmgr/ajax/list_patterns_per_owner.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_hostnames_per_owner(request):
    """
    Description:
        get all hostnames for a given Owner.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            owner_id = request.GET['client_response']
            owner = Owner.objects.get(id=owner_id)
            queryset = owner.get_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_owner.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_patterns_per_project(request):
    """
    Description:
        get all patterns for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            project = Project.objects.get(id=obj_id)
            queryset = project.get_patterns()
            template = loader.get_template('hostmgr/ajax/list_patterns_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_hostnames_per_project(request):
    """
    Description:
        get all hostnames for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            project = Project.objects.get(id=obj_id)
            queryset = project.get_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_assigned_hostnames_per_project(request):
    """
    Description:
        get all hostnames with a status of 'assigned' for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            project = Project.objects.get(id=obj_id)
            queryset = project.get_assigned_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_available_hostnames_per_project(request):
    """
    Description:
        get all hostnames with a status of 'available' for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            project = Project.objects.get(id=obj_id)
            queryset = project.get_expired_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_expired_hostnames_per_project(request):
    """
    Description:
        get all hostnames with a status of 'expired' for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            project = Project.objects.get(id=obj_id)
            queryset = project.get_expired_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_reserved_hostnames_per_project(request):
    """
    Description:
        get all hostnames with a status of 'reserved' for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            project = Project.objects.get(id=obj_id)
            queryset = project.get_reserved_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_hostnames_per_pattern(request):
    """
    Description:
        get all hostnames for a given Pattern.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            pattern = Pattern.objects.get(id=obj_id)
            queryset = pattern.get_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_assigned_hostnames_per_pattern(request):
    """
    Description:
        get all hostnames with a status of 'assigned' for a given Pattern.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            pattern = Pattern.objects.get(id=obj_id)
            queryset = pattern.get_assigned_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_available_hostnames_per_pattern(request):
    """
    Description:
        get all hostnames with a status of 'available' for a given Pattern.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            pattern = Pattern.objects.get(id=obj_id)
            queryset = pattern.get_expired_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_expired_hostnames_per_pattern(request):
    """
    Description:
        get all hostnames with a status of 'expired' for a given Pattern.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            project = Project.objects.get(id=obj_id)
            queryset = project.get_expired_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_reserved_hostnames_per_pattern(request):
    """
    Description:
        get all hostnames with a status of 'reserved' for a given Project.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            pattern = Pattern.objects.get(id=obj_id)
            queryset = pattern.get_reserved_hostnames()
            template = loader.get_template('hostmgr/ajax/list_hostnames_per_project.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)
