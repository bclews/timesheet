from datetime import datetime
from venv import create
import calculations
import parse
import json

FILENAME = 'flex_timesheet.json'

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

#
# File handling...
#
def retrieve_timesheets():
    with open(FILENAME) as timesheet_file:
        return json.load(timesheet_file)

def save_timesheets(timesheet):
    with open(FILENAME, 'w') as timesheet_file:
        timesheet_json = json.dumps(timesheet, indent=4)
        timesheet_file.write(timesheet_json)


#
# Timesheet handling...
#
def get_week_start(the_date):
    parsed_date = parse.get_date(the_date)
    return calculations.find_date_of_previous_monday(parsed_date)

def create_event_log(time_start, time_end, the_date):
    start = parse.get_datetime(the_date, time_start)
    end = parse.get_datetime(the_date, time_end)
    return {"start": start.isoformat(), "end": end.isoformat()}

def add_event(event_type, time_start, time_end, the_date):
    # TODO: check event_type in [work, flex, holiday, sick]
    # TODO: what happens if no timesheet entry for starting date?

    event_log = create_event_log(time_start, time_end, the_date)
    week_start = get_week_start(the_date)
    
    timesheets = retrieve_timesheets()
    for timesheet in timesheets:
        timesheet_week_starting_date = parse.get_date(timesheet["week_starting"])

        if timesheet_week_starting_date == week_start: 
            timesheet[event_type].append(event_log)
            save_timesheets(timesheets)
            break

#
#
#
def work(time_start, time_end, the_date):
    try:
        add_event("work", time_start, time_end, the_date)
    except parse.InputException as error:
        print(error)

def flex(time_start, time_end, the_date):
    try:
        add_event("flex", time_start, time_end, the_date)
    except parse.InputException as error:
        print(error)

def sick(time_start, time_end, the_date):
    try:
        add_event("sick", time_start, time_end, the_date)
    except parse.InputException as error:
        print(error)

def holiday(time_start, time_end, the_date):
    try:
        add_event("holiday", time_start, time_end, the_date)
    except parse.InputException as error:
        print(error)