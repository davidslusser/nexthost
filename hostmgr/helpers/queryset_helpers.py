from django.utils import timezone
import datetime


def get_hr_trend_data(queryset, hrs=24, timestamp="created_at", now=None):
    """
    Get counts, per hour, of rows present by time for a given queryset and datetime field.
    ** only use this for sqlite databases as sqlite doesn't have a 'hour' function;
    :param queryset: (queryset) django queryset you want to filter
    :param hrs: (int) number of hours (from now) to get data for
    :param timestamp: (str) name of datetime field to use in filtering
    :param now: (datetime) the 'now' value to use in datetime calculations
    :return: a dictionary containing a queryset count per hour {hour: count}
    """
    if not now:
        now = timezone.now()
    last_day_data = queryset.filter(**{timestamp + "__gte": (now - datetime.timedelta(days=1))})
    data = {}
    for hour in [(now - datetime.timedelta(hours=i)).hour for i in range(0, hrs)]:
        date_diff = now - datetime.timedelta(hours=hour)
        data[date_diff.hour] = last_day_data.filter(**{timestamp + "__hour": hour}).count()
    return data


def get_hr_trend_labels(hrs=24, now=None):
    """
    make hour labels for the hr trend data graph
    :param hrs: (int) number of hours (from now) to get data for
    :param now: (datetime) the 'now' value to use in datetime calculations
    :return: a list if integers representing the hour of the day
    """
    if not now:
        now = timezone.now()
    return [(now - datetime.timedelta(hours=i)).hour for i in range(0, hrs)]
