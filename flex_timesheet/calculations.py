from datetime import datetime, timedelta
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