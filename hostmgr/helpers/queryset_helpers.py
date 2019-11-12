from django.utils import timezone
import datetime


def get_hr_trend_data(queryset, hrs=24, timestamp="created_at"):
    """
    Get counts, per hour, of rows present by time for a given queryset and datetime field.
    ** only use this for sqlite databases as sqlite doesn't have a 'hour' function;
    :param queryset: (queryset) django queryset you want to filter
    :param hrs: (int) number of hours (from now) to get data for
    :param timestamp: (str) name of datetime field to use in filtering
    :return: a dictionary containing a queryset count per hour {hour: count}
    """
    last_day_data = queryset.filter(**{timestamp + "__gte": (timezone.now() - datetime.timedelta(days=1))})
    data = {}
    now = timezone.now()
    for hour in [(now - datetime.timedelta(hours=i)).hour for i in range(0, hrs)]:
        date_diff = now - datetime.timedelta(hours=hour)
        data[date_diff.hour] = last_day_data.filter(**{timestamp + "__hour": hour}).count()
    return data

