from datetime import datetime, date, timedelta

from django.conf import settings

from pytz import timezone


def get_current_date():
    time_zone = settings.TIME_ZONE
    tz = timezone(time_zone)
    current_date = datetime.now(tz).date()
    return current_date


def get_current_time():
    time_zone = settings.TIME_ZONE
    tz = timezone(time_zone)
    current_time = datetime.now(tz).time()
    return current_time


def get_current_date_time():
    time_zone = settings.TIME_ZONE
    tz = timezone(time_zone)
    current_date_time = datetime.now(tz)
    return current_date_time


def generate_dates(start_date: date, end_date: date):
    date_list = []

    while start_date <= end_date:
        date_list.append(start_date)
        start_date += timedelta(days=1)

    return date_list
