from datetime import date, datetime, timedelta
from collections.abc import Iterable

def split_timedelta(duration):
    """
    Splits the timedelta object into hours, minutes and seconds.

    Args:
        duration (datetime.timedelta): a period of time

    Returns:
        hours (int), minutes (int), seconds (int) of the duration
    """
    seconds = getattr(duration, "seconds", 0)
    days = getattr(duration, "days", 0)

    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

def aggregate(periods):
    """
    Aggregates an array of logged time periods. 

    Args:
        periods (array of dictionaries with keys `start`, `end`): a period of time, e.g.

            periods = [
                {"start": "2022-01-10T08:00", "end": "2022-01-10T12:00"},
                {"start": "2022-01-10T13:00", "end": "2022-01-10T16:40"},
            ]

    Returns:
        hours (int), minutes (int), seconds (int) of the duration
    """
    if not isinstance(periods, Iterable):
        return 0, 0, 0

    timedeltas = list()
    for period in periods:
        if all(key in period for key in ("start", "end")):
            start = datetime.fromisoformat(period["start"])
            end = datetime.fromisoformat(period["end"])
            timedeltas.append(end-start)

    aggregate = sum(timedeltas, timedelta())
    return split_timedelta(aggregate)

def find_date_of_previous_monday(given_date):
    """
    Finds the date of the most recent Monday. If the date is for a Monday then this
    method will return that exact date. For example if `given_date` is Monday 7th Febraury 2022 
    then this method will return Monday 7th Febraury 2022.

    Args:
        given_date (date): a period of time, e.g.

    Returns:
        date (date) of the most recent Monday to have passed
    """ 
    if not isinstance(given_date, date):
        raise TypeError(f"`given_date` should be a date type, not {type(given_date)}")
    
    return given_date - timedelta(days=given_date.weekday())

def find_date_of_next_monday(given_date):
    """
    Finds the date of the next Monday. If the date is for a Monday then this
    method will return the date of the next Monday. For example if `given_date` is
    Monday 7th Febraury 2022 then this method will return Monday 14th Febraury 2022.

    Args:
        given_date (date): a period of time, e.g.

    Returns:
        date (date) of the next upcoming Monday
    """      
    if not isinstance(given_date, date):
        raise TypeError(f"`given_date` should be a date type, not {type(given_date)}")

    return given_date + timedelta(days=-given_date.weekday(), weeks=1)
