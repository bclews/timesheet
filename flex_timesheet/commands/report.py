from datetime import timedelta, datetime
import typer
from flex_timesheet.common import calculations, configuration, parse
import flex_timesheet.common.timesheet as ts


def get_timesheet_data():
    try:
        config_path = configuration.get_default_config_path()
        config_data = configuration.read(config_path)
        timesheet_file_path = configuration.get_timesheet_file(config_data)
        return ts.retrieve_timesheet_file(timesheet_file_path)
    except FileNotFoundError as e:
        typer.echo(e)
        raise typer.Exit(code=1)


def format_hours_and_minutes(hours, minutes):
    return f"{hours} hours, {minutes} minutes"


def report():
    timesheet_file = get_timesheet_data()

    standard_weekly_hours = timedelta(
        hours=timesheet_file["standard_working_hours_per_week"]["hours"],
        minutes=timesheet_file["standard_working_hours_per_week"]["minutes"],
    )

    starting_flextime_balance = timedelta(
        hours=timesheet_file["flextime_balance"]["days"],
        minutes=timesheet_file["flextime_balance"]["seconds"],
    )

    total_flex = timedelta(seconds=0)
    report = []

    for timesheet in timesheet_file["timesheets"]:
        week_starting = parse.get_date(timesheet["week_starting"])

        work = calculations.aggregate(timesheet["work"])
        holiday = calculations.aggregate(timesheet["holiday"])
        sick = calculations.aggregate(timesheet["sick"])
        total_hours = calculations.aggregate_timedeltas([work, holiday, sick])

        weekly_flex = total_hours - standard_weekly_hours
        total_flex += weekly_flex

        hours_work, minutes_work, _ = calculations.split_timedelta(work)
        hours_holiday, minutes_holiday, _ = calculations.split_timedelta(holiday)
        hours_sick, minutes_sick, _ = calculations.split_timedelta(sick)
        hours_total, minutes_total, _ = calculations.split_timedelta(total_hours)
        hours_flex, minutes_flex, _ = calculations.split_timedelta(weekly_flex)

        report.extend(
            [
                typer.style("Week starting: ", bold=True)
                + typer.style(
                    week_starting.strftime("%Y-%m-%d"), fg=typer.colors.MAGENTA
                ),
                typer.style("Hours accounted for: ", bold=True)
                + typer.style(
                    format_hours_and_minutes(hours_total, minutes_total),
                    fg=typer.colors.MAGENTA,
                ),
                typer.style("               work: ", bold=True)
                + format_hours_and_minutes(hours_work, minutes_work),
                typer.style("            holiday: ", bold=True)
                + format_hours_and_minutes(hours_holiday, minutes_holiday),
                typer.style("               sick: ", bold=True)
                + format_hours_and_minutes(hours_sick, minutes_sick),
                typer.style("       accrued flex: ", bold=True)
                + format_hours_and_minutes(hours_flex, minutes_flex),
                "",
            ]
        )

    total_hours_flex, total_minutes_flex, _ = calculations.split_timedelta(
        total_flex + starting_flextime_balance
    )
    report.append(
        typer.style("Total flex: ", bold=True)
        + format_hours_and_minutes(total_hours_flex, total_minutes_flex)
    )

    typer.echo("\n".join(report))


def show_entries(date):
    week_start = ts.get_week_start(date)
    timesheet_file = get_timesheet_data()

    report = []
    for timesheet in timesheet_file["timesheets"]:
        # find existing timesheets
        if parse.get_date(timesheet["week_starting"]) == week_start:
            # timesheet found, so print entries for that week
            report.append(
                typer.style("Week starting: ", bold=True)
                + typer.style(week_start.strftime("%Y-%m-%d"), fg=typer.colors.MAGENTA)
            )
            for event_type in ["work", "holiday", "sick"]:
                for event in timesheet[event_type]:
                    start = datetime.fromisoformat(event["start"])
                    end = datetime.fromisoformat(event["end"])
                    report.append(
                        typer.style(event_type, bold=True)
                        + f" from {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%Y-%m-%d %H:%M')}"
                    )
            typer.echo("\n".join(report))
