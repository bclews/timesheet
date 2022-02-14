from datetime import datetime


class InputException(Exception):
    def __init__(self, message):
        super().__init__(message)


def invalid_time(the_time):
    timeformat = "%H:%M"
    try:
        datetime.strptime(the_time, timeformat)
    except ValueError:
        return True
    return False


def invalid_date(the_date):
    dateformat = "%Y-%m-%d"
    try:
        datetime.strptime(the_date, dateformat)
    except ValueError:
        return True
    return False


def get_datetime(the_date, the_time):
    if invalid_date(the_date):
        raise InputException("The date must be of format YYYY-mm-dd, e.g. 2021-01-12")

    if invalid_time(the_time):
        raise InputException("The time must be of format HH:MM, e.g. 08:00 or 17:00")

    return datetime.strptime(f"{the_date} {the_time}", "%Y-%m-%d %H:%M")
