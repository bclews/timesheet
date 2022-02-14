from ast import Try
import parse
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


def work(time_start, time_end, the_date):
    try:
        start = parse.get_datetime(the_date, time_start)
        end = parse.get_datetime(the_date, time_end)

        print(f"{start.isoformat() =}")
        print(f"{end.isoformat() =}")
    except parse.InputException as error:
        print(error)
