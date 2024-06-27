from datetime import timedelta

import typer
from flex_timesheet.common import calculations, configuration, parse
import flex_timesheet.common.timesheet as ts


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
def report():
    # TODO: remove the flex entry from the timesheet.json - we do not need to record flex

    try:
        config_path = configuration.get_default_config_path()
        config_data = configuration.read(config_path)

        timesheet_file_path = configuration.get_timesheet_file(config_data)
        timesheet_file = ts.retrieve_timesheet_file(timesheet_file_path)
    except FileNotFoundError as e:
        typer.echo(e)
        raise typer.Exit(code=1)

    # Get standard weekly hours
    standard_weekly_hours = timedelta(
        hours=timesheet_file["standard_working_hours_per_week"]["hours"],
        minutes=timesheet_file["standard_working_hours_per_week"]["minutes"],
    )

    report = []
    total_flex = timedelta(seconds=0)
    for timesheet in timesheet_file["timesheets"]:
        aggregate_week_work = calculations.aggregate(timesheet["work"])
        aggregate_week_holiday = calculations.aggregate(timesheet["holiday"])
        aggregate_week_sick = calculations.aggregate(timesheet["sick"])
        aggregate_week = calculations.aggregate_timedeltas(
            [aggregate_week_work, aggregate_week_holiday, aggregate_week_sick]
        )

        hours_work, minutes_work, _ = calculations.split_timedelta(aggregate_week_work)
        hours_holiday, minutes_holiday, _ = calculations.split_timedelta(
            aggregate_week_holiday
        )
        hours_sick, minutes_sick, _ = calculations.split_timedelta(aggregate_week_sick)
        hours_total, minutes_total, _ = calculations.split_timedelta(aggregate_week)

        # TODO: There is an error with this calculation
        # For week starting 2022-06-13 I accounted for 34 hours, 27 minutes
        # For a standard working week of 36 hours 45 minutes, this should result in a deficit of 2.3 hours, not -3 hours 42 minutes
        weekly_accumulated_flex = aggregate_week - standard_weekly_hours
        hours_flex, minutes_flex, _ = calculations.split_timedelta(
            weekly_accumulated_flex
        )
        total_flex += weekly_accumulated_flex

        week_starting = parse.get_date(timesheet["week_starting"])
        report.append(
            typer.style("Week starting: ", bold=True)
            + typer.style(week_starting.strftime("%Y-%m-%d"), fg=typer.colors.MAGENTA)
        )
        report.append(
            typer.style("Hours accounted for: ", bold=True)
            + typer.style(
                f"{hours_total} hours, {minutes_total} minutes", fg=typer.colors.MAGENTA
            )
        )
        report.append(
            typer.style("               work: ", bold=True)
            + f"{hours_work} hours, {minutes_work} minutes"
        )
        report.append(
            typer.style("            holiday: ", bold=True)
            + f"{hours_holiday} hours, {minutes_holiday} minutes"
        )
        report.append(
            typer.style("               sick: ", bold=True)
            + f"{hours_sick} hours, {minutes_sick} minutes"
        )
        report.append(
            typer.style("       accrued flex: ", bold=True)
            + f"{hours_flex} hours, {minutes_flex} minutes"
        )
        report.append("")

    starting_flextime_balance = timedelta(
        hours=timesheet_file["flextime_balance"]["days"],
        minutes=timesheet_file["flextime_balance"]["seconds"],
    )

    total_hours_flex, total_minutes_flex, _ = calculations.split_timedelta(
        total_flex + starting_flextime_balance
    )
    report.append(
        typer.style("Total flex: ", bold=True)
        + f"{total_hours_flex} hours, {total_minutes_flex} minutes"
    )

    return report
