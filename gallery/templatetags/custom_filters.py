from django import template
from django.conf import settings
from datetime import date, timedelta
#from news.models import News

import os
from PIL import Image

register = template.Library()

# TODO: These are from the vans EMEA site - and written quite a while ago.
# some of them are redundant due to django upgrades, others probably not
# required based on the new code. These may/may not want refactored out ~jaymz


__EU__ = 4

__MONTH_NAMES__ = {
                   1 : 'january',
                   2 : 'february',
                   3 : 'march',
                   4 : 'april',
                   5 : 'may',
                   6 : 'june',
                   7 : 'july',
                   8 : 'august',
                   9 : 'september',
                   10 : 'october',
                   11 : 'november',
                   12 : 'december',
                   }

def monthname(value):
    return __MONTH_NAMES__[value]
register.filter('monthname', monthname)

@register.filter
def split(str,splitter):
    return str.split(splitter)

@register.filter
def live_thumbnail(file, size=settings.GALLERY['DEFAULT_THUMBSIZE']):
    miniature_url = None
    x, y = [int(x) for x in size.split('x')]
    try:
        filehead, filetail = os.path.split(file.path)
        basename, format = os.path.splitext(filetail)
        miniature = basename + '_' + size + format
        filename = file.path
        miniature_filename = os.path.join(filehead, miniature)
        filehead, filetail = os.path.split(file.url)
        miniature_url = filehead + '/' + miniature
        if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
        # if the image wasn't already resized, resize it
        if not os.path.exists(miniature_filename):
            image = Image.open(filename)
            image.thumbnail([x, y], Image.ANTIALIAS)
            image.save(miniature_filename, image.format, quality=90, optimize=1)
    except AttributeError:
        pass

    return miniature_url


#the following is sourced from http://www.djangosnippets.org/snippets/129/
def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)

def next_month(d):
    m = d.month
    y = d.year
    return date(y,m,1) + timedelta(days=31)

def prev_month(d):
    m = d.month
    y = d.year
    return date(y,m,1) - timedelta(days=5)

def month_cal(year=date.today().year, month=date.today().month, country_filter=18):
    event_list = News.objects.all().filter(country__id=country_filter, start__year=year, start__month=month, category=3)
    main_list =  MainEvent.objects.all().filter(country__id=country_filter, start_date__month=month, start_date__year=year)
    eu_event_list = News.objects.all().filter(country__id=__EU__, start__year=year, start__month=month, category=3)
    eu_main_list =  MainEvent.objects.all().filter(country__id=__EU__, start_date__month=month, start_date__year=year)

    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    month_cal = []
    week = []
    week_headers = []

    today = date.today()

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        cal_day['today'] = False

        for event in event_list:
            if event.start != None:
                if day == event.start.date():
                    cal_day['event'] = True

            if event.end != None:
                if day >= event.start.date() and day <= event.end.date():
                    cal_day['event'] = True

        for event in main_list:
            try:
                if event.start_date != None:
                    if day >= event.start_date and day <= event.end_date:
                        cal_day['event'] = True
            except:
                pass

        for event in eu_event_list:
            if event.start != None:
                if day >= event.start.date() and day <= event.start.date():
                    cal_day['event'] = True

        for event in eu_main_list:
            try:
                if event.start_date != None:
                    if day >= event.start_date and day <= event.end_date:
                        cal_day['event'] = True
            except:
                pass
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False

        if day == today:
            cal_day['today'] = True

        week.append(cal_day)
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)

    prevmonth = prev_month(first_day_of_month)
    nextmonth = next_month(first_day_of_month)

    return {'calendar': month_cal, 'headers': week_headers, 'month': month, 'year':year, 'first':first_day_of_month, 'nextmonth':nextmonth, 'prevmonth':prevmonth}

register.inclusion_tag('feeds/calendar_output.html')(month_cal)
