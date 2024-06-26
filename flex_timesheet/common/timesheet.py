import json

from flex_timesheet.common import calculations, configuration, parse


def retrieve_timesheet_file():
    timesheet_file = configuration.get_timesheet_file()
    with open(timesheet_file) as timesheet_file:
        return json.load(timesheet_file)


def save_timesheet_file(timesheets):
    sorted_timesheets = sort(timesheets)

    timesheet_file = configuration.get_timesheet_file()
    with open(timesheet_file, "w") as timesheet_file:
        timesheet_json = json.dumps(sorted_timesheets, indent=4)
        timesheet_file.write(timesheet_json)


def sort(timesheets):
    return {
        "standard_working_hours_per_week": timesheets[
            "standard_working_hours_per_week"
        ],
        "flextime_balance": timesheets["flextime_balance"],
        "timesheets": sorted(
            timesheets["timesheets"], key=lambda d: d["week_starting"]
        ),
    }


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
