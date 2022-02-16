from datetime import datetime
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

def retrieve_timesheets():
    with open(FILENAME) as timesheet_file:
        return json.load(timesheet_file)

def save_timesheets(timesheet):
    with open(FILENAME, 'w') as timesheet_file:
        timesheet_json = json.dumps(timesheet, indent=4)
        timesheet_file.write(timesheet_json)

def work(time_start, time_end, the_date):
    try:
        work_start = parse.get_datetime(the_date, time_start)
        work_end = parse.get_datetime(the_date, time_end)
        work = {"start": work_start.isoformat(), "end": work_end.isoformat()}
        
        work_date = parse.get_date(the_date)
        work_week_starting_date = calculations.find_date_of_previous_monday(work_date)

        timesheets = retrieve_timesheets()
        for timesheet in timesheets:
            timesheet_week_starting_date = parse.get_date(timesheet["week_starting"])

            if timesheet_week_starting_date == work_week_starting_date:
                timesheet["work"].append(work)
                save_timesheets(timesheets)
                break
    except parse.InputException as error:
        print(error)
