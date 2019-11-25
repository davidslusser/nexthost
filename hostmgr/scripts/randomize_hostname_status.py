#!/usr/bin/env python

"""
This script will update the status of hostnames selected randomly. This is used to create variation for demo purposes.

Usage Examples:
    python randomize_hostname_status.py --min_count 2 --man_count 15
    python randomize_hostname_status.py --verbose
"""

__version__ = "0.0.1"

# import system modules
import sys
import os
import random
import environ
import argparse
import logging
import traceback
import datetime
import django
from django.utils import timezone

# setup django
sys.path.append(str(environ.Path(__file__) - 3))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexthost.settings")
django.setup()

# import models
from django.contrib.auth.models import (User)
from hostmgr.models import (AssetIdType, Hostname)


def get_opts():
    """ Return an argparse object """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--verbose', default=logging.INFO, action='store_const',
                        const=logging.DEBUG, help='enable debug logging')
    parser.add_argument('--version', action='version', version=__version__, help='show version and exit')
    parser.add_argument('--min_count', required=False, default=2, type=int)
    parser.add_argument('--max_count', required=False, default=10, type=int)
    args = parser.parse_args()
    logging.basicConfig(level=args.verbose)
    return args


def randomize_hostname_status(min_count=2, max_count=10):
    """ create/update/delete some random hostnames """
    # use admin user 'automation_user' to perform actions on hostnames
    auto_user, is_new = User.objects.update_or_create(username="automation_user",
                                                      defaults=dict(
                                                          username="automation_user",
                                                          is_staff=True,
                                                          is_active=True,
                                                          is_superuser=True
                                                      ))
    if not is_new:
        logging.debug("using existing admin user '{}'".format(auto_user))
    else:
        logging.debug("created new admin user '{}'".format(auto_user))

    # get or create a serial number AssetIdType to use for assignments
    asset_id_type, is_new = AssetIdType.objects.get_or_create(name="serial number",
                                                              defaults=dict(name="serial number",
                                                                            description="device serial number")
                                                              )
    if not is_new:
        logging.debug("using existing asset ID type '{}'".format(auto_user))
    else:
        logging.debug("created new asset ID type '{}'".format(auto_user))

    # assign some random 'available' hostnames
    logging.debug("assign some random 'available' hostnames")
    available_hostname_id_list = [h.id for h in Hostname.objects.filter(status='available', persistent=False)]
    for i in range(1, random.randint(min_count, max_count)):
        if i < len(available_hostname_id_list):
            asset_id = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 6)) + str(i)
            h = Hostname.objects.get(id=random.choice(available_hostname_id_list))
            h.assign_hostname(user=auto_user, asset_id_type_name="serial number", asset_id=asset_id)
            available_hostname_id_list.remove(h.id)
            logging.debug("set available hostname {} status to 'assigned'".format(h.hostname))

    # assign some random 'reserved' hostnames
    logging.debug("assign some random 'reserved' hostnames")
    reserved_hostname_id_list = [h.id for h in Hostname.objects.filter(status='reserved', persistent=False)]
    for i in range(1, random.randint(min_count, max_count)):
        if i < len(reserved_hostname_id_list):
            asset_id = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 6)) + str(i)
            h = Hostname.objects.get(id=random.choice(reserved_hostname_id_list))
            h.assign_hostname(user=auto_user, asset_id_type_name="serial number", asset_id=asset_id)
            reserved_hostname_id_list.remove(h.id)
            logging.debug("set reserved hostname {} status to 'assigned'".format(h.hostname))

    # reserve some random 'available' hostnames
    logging.debug("reserve some random 'available' hostnames")
    available_hostname_id_list = [h.id for h in Hostname.objects.filter(status='available', persistent=False)]
    for i in range(1, random.randint(min_count, max_count)):
        if i < len(available_hostname_id_list):
            h = Hostname.objects.get(id=random.choice(available_hostname_id_list))
            h.reserve_hostname(user=auto_user)
            available_hostname_id_list.remove(h.id)
            logging.debug("set available {} status to 'reserved'".format(h.hostname))

    # release some random 'assigned' hostnames
    logging.debug("release some random 'assigned' hostnames")
    assigned_hostname_id_list = [h.id for h in Hostname.objects.filter(status='assigned', persistent=False)]
    for i in range(1, random.randint(min_count, max_count)):
        if i < len(assigned_hostname_id_list):
            h = Hostname.objects.get(id=random.choice(assigned_hostname_id_list))
            h.release_hostname(user=auto_user)
            assigned_hostname_id_list.remove(h.id)
            logging.debug("set assigned hostname {} status to 'available'".format(h.hostname))

    # release some random 'reserved' hostnames
    logging.debug("release some random 'reserved' hostnames")
    reserved_hostname_id_list = [h.id for h in Hostname.objects.filter(status='reserved', persistent=False)]
    for i in range(1, random.randint(min_count, max_count)):
        if i < len(reserved_hostname_id_list):
            h = Hostname.objects.get(id=random.choice(reserved_hostname_id_list))
            h.release_hostname(user=auto_user)
            reserved_hostname_id_list.remove(h.id)
            logging.debug("set reserved {} status to 'available'".format(h.hostname))

    # add assignment_expires datetime for some assigned hostnames
    logging.debug("set expired datetime for some 'assigned' hostnames")
    assigned_hostname_id_list = [h.id for h in Hostname.objects.filter(status='assigned', persistent=False)]
    for i in range(1, random.randint(min_count, max_count)):
        if i < len(assigned_hostname_id_list):
            expires_datetime = timezone.now() + datetime.timedelta(days=random.randint(1, 7))
            h = Hostname.objects.get(id=random.choice(assigned_hostname_id_list))
            h.assignment_expires = expires_datetime
            h.save()
            assigned_hostname_id_list.remove(h.id)
            logging.debug("set assignment_expired on {} to '{}'".format(h.hostname, expires_datetime))


def main():
    """ script entry point """
    opts = get_opts()
    try:
        logging.info('Starting hostname status randomization...')
        randomize_hostname_status(opts.min_count, opts.max_count)
        logging.info('Done!')
    except Exception as err:
        logging.error(err)
        traceback.print_exc()
        return 255


if __name__ == "__main__":
    sys.exit(main())

