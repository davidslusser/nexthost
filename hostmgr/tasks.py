import random

from celery.schedules import crontab
from celery.task import periodic_task

# import models
from django.contrib.auth.models import User
from .models import (AssetIdType, Hostname)


@periodic_task(run_every=(crontab(minute='*/1')))
def randomize_hostname_status():
    """ every 15 minutes, create/update/delete some random hostnames """
    # use admin user 'automation_user' to perform actions on hostnames
    auto_user = User.objects.update_or_create(username="automation_user",
                                              defaults=dict(
                                                  username="automation_user",
                                                  is_staff=True,
                                                  is_active=True,
                                                  is_superuser=True
                                              ))[0]

    # get or create a serial number AssetIdType to use for assignments
    AssetIdType.objects.get_or_create(name="serial number",
                                      defaults=dict(name="serial number",
                                                    description="device serial number")
                                      )

    # assign some random 'available' hostnames
    available_hostname_id_list = [h.id for h in Hostname.objects.filter(status='available', persistent=False)]
    for i in range(1, random.randint(2, 10)):
        asset_id = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 6)) + str(i)
        h = Hostname.objects.get(id=random.choice(available_hostname_id_list))
        h.assign_hostname(user=auto_user, asset_id_type_name="serial number", asset_id=asset_id)
        available_hostname_id_list.remove(h.id)

    # assign some random 'reserved' hostnames
    reserved_hostname_id_list = [h.id for h in Hostname.objects.filter(status='reserved', persistent=False)]
    for i in range(1, random.randint(2, 10)):
        asset_id = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 6)) + str(i)
        h = Hostname.objects.get(id=random.choice(reserved_hostname_id_list))
        h.assign_hostname(user=auto_user, asset_id_type_name="serial number", asset_id=asset_id)
        reserved_hostname_id_list.remove(h.id)

    # reserve some random 'available' hostnames
    available_hostname_id_list = [h.id for h in Hostname.objects.filter(status='available', persistent=False)]
    for i in range(1, random.randint(2, 15)):
        h = Hostname.objects.get(id=random.choice(available_hostname_id_list))
        h.reserve_hostname(user=auto_user)
        available_hostname_id_list.remove(h.id)

    # release some random 'assgined' hostnames
    assigned_hostname_id_list = [h.id for h in Hostname.objects.filter(status='assigned', persistent=False)]
    for i in range(1, random.randint(2, 15)):
        h = Hostname.objects.get(id=random.choice(assigned_hostname_id_list))
        h.release_hostname(user=auto_user)
        assigned_hostname_id_list.remove(h.id)

    # release some random 'reserved' hostnames
    reserved_hostname_id_list = [h.id for h in Hostname.objects.filter(status='assigned', persistent=False)]
    for i in range(1, random.randint(2, 15)):
        h = Hostname.objects.get(id=random.choice(reserved_hostname_id_list))
        h.release_hostname(user=auto_user)
        reserved_hostname_id_list.remove(h.id)
