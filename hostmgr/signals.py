from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import sys
import random

# import models
from django.contrib.auth.models import (Group, User)
from hostmgr.models import (Pattern)


def get_random_row(queryset):
    """ return a single, random entry from a queryset """
    random_index = random.randint(0, queryset.count() - 1)
    return queryset[random_index]


@receiver(post_save, sender=Pattern, dispatch_uid="add hostnames to pattern")
def add_hostnames_for_patterm(sender, instance, created, **kwargs):
    """ create hostnames for a given Pattern """
    # do not execute signal when running tests
    if 'manage.py' in sys.argv[0] and 'test' in sys.argv:
        return
    instance.create_hosts()


@receiver(post_save, sender=User, dispatch_uid="add groups to new user")
def add_groups_to_new_user(sender, instance, created, **kwargs):
    """ add new user to some random groups """
    # do not execute signal when running tests
    if 'manage.py' in sys.argv[0] and 'test' in sys.argv:
        return
    if created:
        group_list = Group.objects.all()
        group_count = random.randint(1, len(group_list))
        for i in range(0, group_count):
            group = get_random_row(group_list)
            group.user_set.add(instance)
