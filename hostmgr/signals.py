from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import sys

# import models
from hostmgr.models import (Pattern)


@receiver(post_save, sender=Pattern, dispatch_uid="add hostnames to pattern")
def add_hostnames_for_patterm(sender, instance, created, **kwargs):
    """ create hostnames for a given Pattern """
    # do not execute signal when running tests
    if 'manage.py' in sys.argv[0] and 'test' in sys.argv:
        return
    instance.create_hosts()
