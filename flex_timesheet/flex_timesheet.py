import calculations
import parse
import json
import typer
from datetime import timedelta

FILENAME = "flex_timesheet.json"

#
# File handling...
#
def sort(timesheets):
    return {
        "standard_working_hours_per_week" : timesheets["standard_working_hours_per_week"],
        "flextime_balance" : timesheets["flextime_balance"],
        "timesheets" : sorted(timesheets["timesheets"], key=lambda d: d['week_starting'])
    }

def retrieve_timesheet_file():
    with open(FILENAME) as timesheet_file:
        return json.load(timesheet_file)


def save_timesheet_file(timesheets):
    sorted_timesheets = sort(timesheets)
    with open(FILENAME, "w") as timesheet_file:
        timesheet_json = json.dumps(sorted_timesheets, indent=4)
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
        # find existing timesheets
        if parse.get_date(timesheet["week_starting"]) == week_start:
            timesheet[event_type].append(event_log)
            save_timesheet_file(timesheet_file)
            break
    else:
        # a timesheets does not yet exist for the given date, so create a new one
        timesheet = create_new_timesheet(week_start, event_type, event_log)
        timesheet_file['timesheets'].append(timesheet)
        save_timesheet_file(timesheet_file)

#
# Timesheet reporting...
#
# Week starting: 28th February 2022
# Starting flextime balance: 2 hours, 22 minutes
# Total logged hours: 33 hours, 33 minutes
#
# Hours work: 22 hours, 22 minutes
#        Monday 08:00-12:00 
#        Monday 13:00-17:00
#       Tuesday 08:00-12:00 
#       Tuesday 13:00-17:00
#     Wednesday 08:00-12:00 
#     Wednesday 13:00-17:00
#      Thursday 08:00-12:00 
#      Thursday 13:00-17:00
#        Friday 08:00-12:00 
#        Friday 13:00-17:00
#
# Hours flex: 0 hours, 0 minutes
#
# Hours holiday: 0 hours, 0 minutes
#
# Hours sick: 0 hours, 0 minutes
def report(the_date):
    #TODO: remove the flex entry from the timesheet.json - we do not need to record flex

    timesheet_file = retrieve_timesheet_file()

    # Get standard weekly hours
    standard_weekly_hours = timedelta(
        hours=timesheet_file["standard_working_hours_per_week"]["hours"], 
        minutes=timesheet_file["standard_working_hours_per_week"]["minutes"]
    )

    report = []
    total_flex = timedelta(seconds=0)
    for timesheet in timesheet_file["timesheets"]:
        aggregate_week_work = calculations.aggregate(timesheet["work"])
        aggregate_week_holiday = calculations.aggregate(timesheet["holiday"])
        aggregate_week_sick = calculations.aggregate(timesheet["sick"])
        aggregate_week = calculations.aggregate_timedeltas([aggregate_week_work, aggregate_week_holiday, aggregate_week_sick])

        hours_work, minutes_work, seconds_work = calculations.split_timedelta(aggregate_week_work)
        hours_holiday, minutes_holiday, seconds_holiday = calculations.split_timedelta(aggregate_week_holiday)
        hours_sick, minutes_sick, seconds_sick = calculations.split_timedelta(aggregate_week_sick)
        hours_total, minutes_total, seconds_total = calculations.split_timedelta(aggregate_week)

        # TODO: There is an error with this calculation
        # For week starting 2022-06-13 I accounted for 34 hours, 27 minutes
        # For a standard working week of 36 hours 45 minutes, this should result in a deficit of 2.3 hours, not -3 hours 42 minutes
        weekly_accumulated_flex =  aggregate_week - standard_weekly_hours
        hours_flex, minutes_flex, seconds_total = calculations.split_timedelta(weekly_accumulated_flex)
        total_flex += weekly_accumulated_flex

        week_starting = parse.get_date(timesheet["week_starting"])
        report.append( typer.style(f"Week starting: ", bold=True) + typer.style(week_starting.strftime("%Y-%m-%d"), fg=typer.colors.MAGENTA))
        report.append(typer.style(f"Hours accounted for: ", bold=True) + typer.style(f"{hours_total} hours, {minutes_total} minutes", fg=typer.colors.MAGENTA))
        report.append(typer.style(f"               work: ", bold=True) + f"{hours_work} hours, {minutes_work} minutes")
        report.append(typer.style(f"            holiday: ", bold=True) + f"{hours_holiday} hours, {minutes_holiday} minutes")
        report.append(typer.style(f"               sick: ", bold=True) + f"{hours_sick} hours, {minutes_sick} minutes")
        report.append(typer.style(f"       accrued flex: ", bold=True) + f"{hours_flex} hours, {minutes_flex} minutes")
        report.append("")


    starting_flextime_balance = timedelta(
        hours=timesheet_file["flextime_balance"]["days"], 
        minutes=timesheet_file["flextime_balance"]["seconds"]
    )

    total_hours_flex, total_minutes_flex, total_seconds_flex = calculations.split_timedelta(total_flex + starting_flextime_balance)
    report.append(typer.style(f"Total flex: ", bold=True) + f"{total_hours_flex} hours, {total_minutes_flex} minutes")

    return report