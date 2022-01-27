from datetime import datetime

# FILENAME = 'should-be-defined-in-a-configuration-file.json'

# WEEKLY_TIMESHEET_TEMPLATE = {
#     "week_starting": "",
#     "standard_working_hours_per_week": {
#         "hours": 36,
#         "minutes": 45,
#         "days_in_working_week": 5
#     },
#     "flextime_balance": {
#         "days": 0,
#         "seconds": 0
#     },
#     "work": [],
#     "flex": [],
#     "holiday": [],
#     "sick": []
# }

# TODO: pull out the date & time validation into its own unit
class InputException(Exception):
    def __init__(self, message):
        super().__init__(message)

def is_date_valid(the_date):
    dateformat = "%Y-%m-%d"
    try:
        datetime.strptime(the_date, dateformat)
    except ValueError:
        return False
    return True

def is_time_valid(the_time):
    timeformat = "%H:%M"
    try:
        datetime.strptime(the_time, timeformat)
    except ValueError:
        return False
    return True

def work(time_start, time_end, the_date):
    # TODO: This body of code will be similar for many other methods.
    #       So break this method down a method called get_datetime_from_string where
    #       you just return one datetime string
    if not is_time_valid(time_start):
        raise InputException("`time_start` must be of format HH:MM, e.g. 08:00 or 17:00")

    if not is_time_valid(time_end):
        raise InputException("`time_end` must be of format HH:MM, e.g. 08:00 or 17:00")

    if not is_date_valid(the_date):
        raise InputException("`date` must be of format YYYY-mm-dd, e.g. 2021-01-12")

    start = datetime.strptime(f"{the_date} {time_start}", "%Y-%m-%d %H:%M")
    end = datetime.strptime(f"{the_date} {time_end}", "%Y-%m-%d %H:%M")

    print(f"{start.isoformat() =}")
    print(f"{end.isoformat() =}")