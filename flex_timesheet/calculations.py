from datetime import date, datetime, timedelta
from collections.abc import Iterable

def split_timedelta(duration):
    """ 
    Splits the timedelta object into hours, minutes and seconds.

    Args:
        duration (datetime.timedelta): a period of time

    Returns:
        hours (int or float) of the duration
        minutes (int or float) of the duration
        seconds (int or float) of the duration
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

    Raises:
        TypeError: `periods` must be of type Iteratable

    Returns:
        hours (int or float) of the duration
        minutes (int or float) of the duration 
        seconds (int or float) of the duration
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
        given_date (datetime.date): find the Monday prior to this date

    Raises:
        TypeError: `given_date` must be of type datetime.date

    Returns:
        date (datetime.date) of the most recent Monday to have passed
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
        given_date (datetime.date): find the Monday after this date

    Raises:
        TypeError: `given_date` must be of type datetime.date

    Returns:
        datetime.date of the next upcoming Monday
    """
    if not isinstance(given_date, date):
        raise TypeError(f"`given_date` should be a date type, not {type(given_date)}")

    return given_date + timedelta(days=-given_date.weekday(), weeks=1)

def is_timedelta_positive(delta):
    """
    Determines if a timedelta onject is positive or negative.

    From the documentation => https://docs.python.org/3/library/datetime.html
        Only days, seconds and microseconds are stored internally.
    And:
        days, seconds and microseconds are then normalized so that the representation 
        is unique, with:
            0 <= microseconds < 1000000
            0 <= seconds < 3600*24 (the number of seconds in one day)
            -999999999 <= days <= 999999999

    Args:
        delta (datetime.timedelta): timedelta to be assessed

    Raises:
        TypeError: `delta` must be of type datetime.timedelta

    Returns:
        [bool]: true if `delta` is >=0, otherwise false
    """
    if not isinstance(delta, timedelta):
        raise TypeError(f"`delta` should be a date type, not {type(delta)}")

    return delta.days >= 0