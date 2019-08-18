from django.urls import reverse
from django.db import models as models
from django.contrib.auth.models import Group
from djangohelpers.managers import HandyHelperModelManager

# import third party modules
from auditlog.registry import auditlog

# import project modules
from hostmgr.exceptions import (UserNotAuthorized, HostnameInactive, InvalidStateTransition, InvalidAssetIdType,
                                HostnamePersistent, AssetIdRequired)


class HostManagerBase(models.Model):
    """ abstract model for common hostmgr db fields """
    objects = HandyHelperModelManager()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="date/time when this row was added")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="date/time when this row was updated")
    active = models.BooleanField(default=True, help_text="select if this record is currently active")

    class Meta:
        abstract = True
        ordering = ('-created_at', )


class Owner(HostManagerBase):
    """ owner table """
    name = models.CharField(max_length=32, unique=True, help_text="name of this group")
    group = models.ForeignKey(Group, help_text="group this owner belongs to", on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True, help_text="group email alias for group")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hostmgr_owner_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('hostmgr_owner_update', args=(self.pk,))

    def get_projects(self):
        """ get all projects for an owner """
        return self.project_set.all()

    def get_patterns(self):
        """ get all patterns for an owner """
        return Pattern.objects.filter(project__owner=self)

    def get_hostnames(self):
        """ get all hostnames for an owner """
        return Hostname.objects.filter(pattern__project__owner=self)

    def get_available_hostnames(self):
        return Hostname.objects.filter(pattern__project__owner=self, status="available")

    def get_assigned_hostnames(self):
        return Hostname.objects.filter(pattern__project__owner=self, status="assigned")

    def get_reserved_hostnames(self):
        return Hostname.objects.filter(pattern__project__owner=self, status="reserved")

    def get_expired_hostnames(self):
        return Hostname.objects.filter(pattern__project__owner=self, status="expired")


class Project(HostManagerBase):
    """ table to track projects """
    name = models.CharField(max_length=255, unique=True, help_text="name of this project")
    owner = models.ForeignKey('hostmgr.Owner', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True, help_text="description of this project")

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

    def get_manageability(self, user):
        """
        Determine if user can manage this object. All admins can manage all projects.
        User can manage project if they are member of the group that owns the project.
        :param user: user object
        :return: (bool) True if user is authorized to manage this project, otherwise False
        """
        user_can_manage = False
        if user.is_superuser:
            user_can_manage = True
        elif user.groups.filter(name=getattr(self.owner.group, 'name', None)):
            user_can_manage = True
        return user_can_manage

    def get_absolute_url(self):
        return reverse('hostmgr_project_detail', args=(self.pk, ))

    def get_update_url(self):
        return reverse('hostmgr_project_update', args=(self.pk, ))

    def get_patterns(self):
        return self.pattern_set.all()

    def get_hostnames(self):
        return Hostname.objects.filter(pattern__project=self)

    def get_available_hostnames(self):
        return Hostname.objects.filter(pattern__project=self, status="available")

    def get_reserved_hostnames(self):
        return Hostname.objects.filter(pattern__project=self, status="reserved")

    def get_assigned_hostnames(self):
        return Hostname.objects.filter(pattern__project=self, status="assigned")

    def get_expired_hostnames(self):
        return Hostname.objects.filter(pattern__project=self, status="expired")


class Pattern(HostManagerBase):
    """ when a pattern is added, generate all hostnames per rules of the pattern and set is_assigned = False"""
    name = models.CharField(max_length=16, unique=True, blank=True, null=True,
                            help_text="name/reference for this hostname pattern")
    description = models.CharField(max_length=255, blank=True, null=True, help_text="description for this pattern")
    project = models.ForeignKey('hostmgr.Project', on_delete=models.CASCADE)
    prefix = models.CharField(max_length=32, help_text="prefix for this hostname patter")
    delimiter = models.CharField(max_length=8, default="", blank=True, null=True,
                                 help_text="character(s) separating prefix and number")
    host_count = models.IntegerField(default=100, help_text="maximum number of hosts for this pattern")
    increment = models.IntegerField(default=1, help_text="increment (integer) in to increment hostnames by")
    start_from = models.IntegerField(default=1, help_text="number in to start hostnames at")

    class Meta:
        unique_together = (("prefix", "delimiter"), )

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

    def get_manageability(self, user):
        """
        Determine if user can manage this object. All admins can manage all paterns.
        User can manage pattern if they are member of the group that owns the project containing the pattern.
        :param user: user object
        :return: (bool) True if user is authorized to manage this hostname, otherwise False
        """
        user_can_manage = False
        if user.is_superuser:
            user_can_manage = True
        elif user.groups.filter(name=getattr(self.project.owner.group, 'name', None)):
            user_can_manage = True
        return user_can_manage

    def build_regex(self):
        """ build the regex value for this pattern """
        return "^{}{}[0-9]{{{}}}$".format(self.prefix, self.delimiter, len(str(self.host_count)))

    def validate_user(self, user):
        """ Check if use is authorized to perform an action (CRUD) on a Pattern. User must be a member of the
        group who owns the project or a superuser """
        pass

    def create_hosts(self):
        """ create hosts entries based on the rules of this hostname pattern """
        for i in range(self.start_from, self.host_count * self.increment + 1, self.increment):
            num = "{}".format(i).zfill(len(str(self.host_count)))
            hostname = "{}{}{}".format(self.prefix, self.delimiter, num)
            Hostname.objects.get_or_create(hostname=hostname,
                                           defaults=dict(hostname=hostname, pattern=self))

    def update_hosts(self):
        """ create/remove host entries based on rule changes (host_counts increase) """
        pass

    def request_hostname(self, count=1, consecutive=False):
        """
        get the next available hostname
        :param count: <int> number of hostnames to get
        :param consecutive: <bool> if True and count > 1, only get hostnames that are consecutive
        :return:
        """
        pass

    def reserve_hostname(self):
        pass

    def release_hostname(self):
        pass

    def extend_hostname(self):
        pass

    def get_available_hostnames(self):
        return self.hostname_set.filter(status="available")

    def get_assigned_hostnames(self):
        return self.hostname_set.filter(status="assigned")

    def get_reserved_hostnames(self):
        return self.hostname_set.filter(status="reserved")

    def get_expired_hostnames(self):
        return self.hostname_set.filter(status="expired")

    # def save(self, *args, **kwargs):
    #     # if not self.pk:
    #     # self.create_hosts()
    #     super().save(*args, **kwargs)


class AssetIdType(HostManagerBase):
    """ table to track types of asset identifications, such as serial number, asset tag, MAC address, etc. """
    name = models.CharField(max_length=128, unique=True, help_text="type of asset identification")
    description = models.CharField(max_length=255, blank=True, null=True, help_text="asset ID type description")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name


class Hostname(HostManagerBase):
    """ A hostname is an entry of a host pattern. Hostnames are generated automatically when a host pattern is
     created or edited. """
    HOST_STATUS_CHOICES = (('available', 'available'), ('assigned', 'assigned'),
                           ('reserved', 'reserved'), ('expired', 'expired'), ('unavailable', 'unavailable'))
    pattern = models.ForeignKey('hostmgr.Pattern', help_text="pattern this hostname was generated from",
                                on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255, unique=True, help_text="name of host")
    asset_id = models.CharField(max_length=255, blank=True, null=True,
                                help_text="unique identifier of the asset using this hostname")
    asset_id_type = models.ForeignKey('hostmgr.AssetIdType', blank=True, null=True, help_text="type of asset ID used",
                                      on_delete=models.CASCADE)
    persistent = models.BooleanField(default=False, help_text="select if hostname can be not reassigned or deleted")
    status = models.CharField(max_length=16, choices=HOST_STATUS_CHOICES, default="available",
                              help_text="status of this hostname")
    reservation_expires = models.DateTimeField(blank=True, null=True, help_text="time when this reservation expires")
    assignment_expires = models.DateTimeField(blank=True, null=True, help_text="time when this assignment expires")

    def __unicode__(self):
        return u'%s' % self.hostname

    def __str__(self):
        return self.hostname

    # class Meta:
    #     unique_together = (("asset_id", "asset_id_type"), )

    def get_manageability(self, user):
        """
        Determine if user can manage this object. All admins can manage all hostnames.
        User can manage hostname if they are member of the group that owns the project containing the
        hostname pattern.
        :param user: user object
        :return: (bool) True if user is authorized to manage this hostname, otherwise False
        """
        user_can_manage = False
        if user.is_superuser:
            user_can_manage = True
        elif user.groups.filter(name=getattr(self.pattern.project.owner.group, 'name', None)):
            user_can_manage = True
        return user_can_manage

    def get_hostname(self, count=1, consecutive=False):
        """
        get the next available hostname(s)
        :param count: (int) number of available hostnames to return
        :param consecutive: (bool) if true return only hostnames with consecutive counts; for example:
        (host-005, host-006, host--006, etc.)
        :return: list of hostnames
        """
        pass

    def reserve_hostname(self, user):
        """ set the status of this host to 'reserved' """
        if not self.get_manageability(user):
            raise UserNotAuthorized("{} is not authorized to manage this lock".format(user))
        if not self.active:
            raise HostnameInactive("{} is currently inactive".format(self.hostname))
        self.status = "reserved"
        self.save()
        return 0

    def assign_hostname(self, user, asset_id, asset_id_type_name, persistent):
        """ set the status of this host to 'assigned' """
        if not self.get_manageability(user):
            raise UserNotAuthorized("{} is not authorized to manage this lock".format(user))
        if not self.active:
            raise HostnameInactive("{} is currently inactive".format(self.hostname))
        if self.status not in ['available', 'reserved']:
            raise InvalidStateTransition("{} has a status of {}; can not transition to 'assigned".
                                         format(self.hostname, self.status))
        if not asset_id:
            raise AssetIdRequired("asset ID required to assign a hostname")

        asset_id_type_obj = AssetIdType.objects.get_object_or_none(name=asset_id_type_name)
        if not asset_id_type_obj:
            raise InvalidAssetIdType("{} is not a valid asset ID type".format(asset_id_type_name))

        self.asset_id = asset_id
        self.asset_id_type = asset_id_type_obj
        if persistent in [True, 'true', 'True']:
            self.persistent = True
        self.status = "assigned"
        self.save()
        return 0

    def reassign_hostname(self, user, asset_id, asset_id_type_name):
        """ assign this hostname to a different asset """
        if not self.get_manageability(user):
            raise UserNotAuthorized("{} is not authorized to manage this lock".format(user))
        if not self.active:
            raise HostnameInactive("{} is currently inactive".format(self.hostname))
        if self.status not in ['assigned']:
            raise InvalidStateTransition("{} has a status of {}; can not transition to 'assigned".
                                         format(self.hostname, self.status))
        asset_id_type_obj = AssetIdType.objects.get_object_or_none(name=asset_id_type_name)
        if not asset_id_type_obj:
            raise InvalidAssetIdType("{} is not a valid asset ID type".format(asset_id_type_name))

        self.asset_id = asset_id
        self.asset_id_type = asset_id_type_obj
        self.status = "assigned"
        self.save()
        return 0

    def release_hostname(self, user):
        """ set the status of this host to 'available' """
        if not self.get_manageability(user):
            raise UserNotAuthorized("{} is not authorized to manage this lock".format(user))
        if not self.active:
            raise HostnameInactive("{} is currently inactive".format(self.hostname))
        if self.persistent:
            raise HostnamePersistent("{} is set to persistent and can not be released".format(self.hostname))
        self.status = "available"
        self.asset_id_type = None
        self.asset_id = None
        self.save()
        return 0


# Models to register with AuditLog
auditlog.register(Owner)
auditlog.register(Project)
auditlog.register(Pattern)
auditlog.register(AssetIdType)
auditlog.register(Hostname)
