from django.urls import reverse
from django.db import models as models
from django.contrib.auth.models import Group
from djangohelpers.managers import HandyHelperModelManager

# import third party modules
from auditlog.registry import auditlog


class HostManagerBase(models.Model):
    """ abstract model for common hostmgr db fields """
    objects = HandyHelperModelManager()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="date/time when this row was added")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="date/time when this row was updated")
    is_active = models.BooleanField(default=True, help_text="select if this record is currently active")

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
        return HostnamePattern.objects.filter(project__owner=self)

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

    def get_absolute_url(self):
        return reverse('hostmgr_project_detail', args=(self.pk, ))

    def get_update_url(self):
        return reverse('hostmgr_project_update', args=(self.pk, ))

    def get_patterns(self):
        return self.hostnamepattern_set.all()

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


class HostnamePattern(HostManagerBase):
    """ when a pattern is added, generate all hostnames per rules of the pattern and set is_assigned = False"""
    name = models.CharField(max_length=16, blank=True, null=True, help_text="name/reference for this hostname pattern")
    description = models.CharField(max_length=255, blank=True, null=True, help_text="description for this pattern")
    project = models.ForeignKey('hostmgr.Project', on_delete=models.CASCADE)
    prefix = models.CharField(max_length=32, help_text="prefix for this hostname patter")
    delimiter = models.CharField(max_length=8, default="", blank=True, null=True,
                                 help_text="character(s) separating prefix and number")
    max_hosts = models.IntegerField(default=100, help_text="maximum number of hosts for this pattern")
    increment = models.IntegerField(default=1, help_text="increment (integer) in to increment hostnames by")
    start_from = models.IntegerField(default=1, help_text="number in to start hostnames at")

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

    def build_regex(self):
        """ build the regex value for this pattern """
        return "^\S+{}[0-9]{{1,{}}}$".format(self.delimiter, len(str(self.max_hosts)))

    def validate_user(self, user):
        """ Check if use is authorized to perform an action (CRUD) on a HostnamePattern. User must be a member of the
        group who owns the project or a superuser """
        pass

    def create_hosts(self):
        """ create hosts entries based on the rules of this hostname pattern """
        for i in range(self.start_from, self.max_hosts * self.increment + 1, self.increment):
            num = "{}".format(i).zfill(len(str(self.max_hosts)))
            hostname = "{}{}{}".format(self.prefix, self.delimiter, num)
            Hostname.objects.get_or_create(hostname=hostname,
                                           defaults=dict(hostname=hostname, pattern=self))

    def update_hosts(self):
        """ create/remove host entries based on rule changes (max_hosts increase) """
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
                           ('reserved', 'reserved'), ('expired', 'expired'))
    pattern = models.ForeignKey('hostmgr.HostnamePattern', help_text="pattern this hostname was generated from",
                                on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255, unique=True, help_text="name of host")
    asset_id = models.CharField(max_length=255, blank=True, null=True,
                                help_text="unique identifier of the asset using this hostname")
    asset_id_type = models.ForeignKey('hostmgr.AssetIdType', blank=True, null=True, help_text="type of asset ID used",
                                      on_delete=models.CASCADE)
    # is_assigned = models.BooleanField(default=False, help_text="set to True when hostname is assigned")
    is_eternal = models.BooleanField(default=False, help_text="select if hostname can be not reassigned or deleted")
    # is_reserved = models.BooleanField(default=False, help_text="select if hostname is reserved, but not assigned")
    #TODO: change flags to status (assigned, reserved, available, expired, etc.)
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


# Models to register with AuditLog
auditlog.register(Owner)
auditlog.register(Project)
auditlog.register(HostnamePattern)
auditlog.register(Hostname)
