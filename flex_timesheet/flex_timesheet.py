import calculations
import parse
import json

FILENAME = "flex_timesheet.json"

#
# File handling...
#
def retrieve_timesheet_file():
    with open(FILENAME) as timesheet_file:
        return json.load(timesheet_file)


def save_timesheet_file(timesheet):
    with open(FILENAME, "w") as timesheet_file:
        timesheet_json = json.dumps(timesheet, indent=4)
        timesheet_file.write(timesheet_json)


#
# Timesheet handling...
#
def create_new_timesheet(the_date, event_type, event_log):
    new_timesheet = {
        "week_starting": the_date.strftime("%Y-%m-%d"),
        "work": [],
        "flex": [],
        "holiday": [],
        "sick": [],
    }
    new_timesheet[event_type].append(event_log)
    return new_timesheet


def get_week_start(the_date):
    parsed_date = parse.get_date(the_date)
    return calculations.find_date_of_previous_monday(parsed_date)


def create_event_log(time_start, time_end, the_date):
    start = parse.get_datetime(the_date, time_start)
    end = parse.get_datetime(the_date, time_end)
    return {"start": start.isoformat(), "end": end.isoformat()}


def add_event(event_type, time_start, time_end, the_date):
    event_log = create_event_log(time_start, time_end, the_date)
    week_start = get_week_start(the_date)

    timesheet_file = retrieve_timesheet_file()
    for timesheet in timesheet_file["timesheets"]:
        # find existing timesheet
        if parse.get_date(timesheet["week_starting"]) == week_start:
            timesheet[event_type].append(event_log)
            save_timesheet_file(timesheet_file)
            break
    else:
        # a timesheet does not yet exist for the given date, so create a new one
        timesheet = create_new_timesheet(week_start, event_type, event_log)
        timesheet_file.append(timesheet)
        save_timesheet_file(timesheet_file)
