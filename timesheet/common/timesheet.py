import json

from timesheet.common import calculations, configuration, parse


def retrieve_timesheet_file(timesheet_file_path):
    with open(timesheet_file_path) as timesheet_file_path:
        return json.load(timesheet_file_path)


def save_timesheet_file(timesheet_file_path, timesheets):
    sorted_timesheets = sort(timesheets)

    with open(timesheet_file_path, "w") as timesheet_file_path:
        timesheet_json = json.dumps(sorted_timesheets, indent=4)
        timesheet_file_path.write(timesheet_json)


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
        "holiday": [],
        "sick": [],
    }
    new_timesheet[event_type].append(event_log)
    return new_timesheet


def get_week_start(the_date):
    parsed_date = parse.get_date(the_date)
    return calculations.find_date_of_previous_monday(parsed_date)


def create_event_log(time_start, time_end, the_date, location=None):
    start = parse.get_datetime(the_date, time_start)
    end = parse.get_datetime(the_date, time_end)

    event_log = {"start": start.isoformat(), "end": end.isoformat()}

    if location is not None:
        event_log["location"] = location

    return event_log
