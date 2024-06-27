from datetime import date
from pathlib import Path

import typer

from flex_timesheet.common import parse
import flex_timesheet.commands.report as r
import flex_timesheet.commands.configuration as c
import flex_timesheet.commands.timesheet as ts

WORK = "work"
FLEX = "flex"
SICK = "sick"
HOLIDAY = "holiday"

app = typer.Typer()


def get_date():
    return date.today()


@app.command()
def configure(
    config_path: Path = typer.Option(None, help="Path to the configuration file"),
):
    """
    Configure the timesheet application.
    """
    try:
        c.configure(config_path)
    except parse.InputException as error:
        typer.echo(error)


@app.command()
def show_config(
    config_path: Path = typer.Option(None, help="Path to the configuration file"),
):
    """
    Show the current configuration settings.
    """
    try:
        c.show_config(config_path)
    except parse.InputException as error:
        typer.echo(error)


@app.command()
def report(date: str = typer.Argument(get_date, help="Default value is today's date.")):
    """
    What is my timesheet looking like? Is it beer o'clock yet?
    """
    r.report()


@app.command()
def show_entries(
    date: str = typer.Argument(get_date, help="Default value is today's date."),
):
    """
    Show the timesheet for week of the given date.
    """
    try:
        r.show_entries(date)
    except parse.InputException as error:
        typer.echo(error)


@app.command()
def work(
    time_start: str = typer.Argument(..., help="Time the period of work started."),
    time_end: str = typer.Argument(..., help="Time the period of work ended."),
    location: str = typer.Argument("Home", help="Location of work. Default is 'Home'."),
    date: str = typer.Argument(get_date, help="Default value is today's date."),
):
    """
    Add a period of work to the timesheet.

    Date should be in current week? If not, how do we retrospectively deal with flex? Easy. Right?
    """
    try:
        ts.add_event(WORK, time_start, time_end, date, location)
    except parse.InputException as error:
        typer.echo(error)


@app.command()
def sick(
    time_start: str = typer.Argument(
        ..., help="Time the period of sick leave started."
    ),
    time_end: str = typer.Argument(..., help="Time the period of sick leave ended."),
    date: str = typer.Argument(get_date, help="Default value is today's date."),
):
    """
    Add a period of sick leave to the timesheet.
    """
    try:
        ts.add_event(SICK, time_start, time_end, date)
    except parse.InputException as error:
        typer.echo(error)


@app.command()
def holiday(
    time_start: str = typer.Argument(..., help="Time the period of holiday started."),
    time_end: str = typer.Argument(..., help="Time the period of holiday ended."),
    date: str = typer.Argument(get_date, help="Default value is today's date."),
):
    """
    Add a period of holiday to the timesheet.
    """
    try:
        ts.add_event(HOLIDAY, time_start, time_end, date)
    except parse.InputException as error:
        typer.echo(error)


if __name__ == "__main_":
    app()
