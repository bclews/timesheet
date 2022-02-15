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
        start = parse.get_datetime(the_date, time_start)
        end = parse.get_datetime(the_date, time_end)
        work = {"start": start.isoformat(), "end": end.isoformat()}

        timesheets = retrieve_timesheets()
        for timesheet in timesheets["time_sheets"]:
            if timesheet["week_starting"] == "2022-02-14":                
                timesheet["work"].append(work)
                save_timesheets(timesheets)
                break
    except parse.InputException as error:
        print(error)
