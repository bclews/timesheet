import typer
import flex_timesheet
from datetime import date

def get_date():
    return date.today()

app = typer.Typer()

@app.command()
def report(
    date: str = typer.Argument(get_date, help="Default value is today's date.")
):
    """
    What is my timesheet looking like? Is it beer o'clock yet?
    """
    typer.echo(f"{date=}")

@app.command()
def work(
    time_start: str = typer.Argument(..., help="Time the period of work started."),
    time_end: str = typer.Argument(..., help="Time the period of work ended."),
    date: str = typer.Argument(get_date, help="Default value is today's date.")
):
    """
    Add a period of work to the timesheet.

    Date should be in current week? If not, how do we retrospectively deal with flex? Easy. Right?
    """
    flex_timesheet.work(time_start, time_end, date)

@app.command()
def flex(
    time_start: str = typer.Argument(..., help="Time the period of flex leave started."),
    time_end: str = typer.Argument(..., help="Time the period of flex leave ended."),
    date: str = typer.Argument(get_date, help="Default value is today's date.")
):
    """
    Add a period of flex to the timesheet.
    """
    typer.echo(f"{time_start=} {time_end=} {date=}")

@app.command()
def sick(
    time_start: str = typer.Argument(..., help="Time the period of sick leave started."),
    time_end: str = typer.Argument(..., help="Time the period of sick leave ended."),
    date: str = typer.Argument(get_date, help="Default value is today's date.")
):
    """
    Add a period of sick leave to the timesheet.
    """
    typer.echo(f"{time_start=} {time_end=} {date=}")

@app.command()
def holiday(
    time_start: str = typer.Argument(..., help="Time the period of holiday started."),
    time_end: str = typer.Argument(..., help="Time the period of holiday ended."),
    date: str = typer.Argument(get_date, help="Default value is today's date.")
):
    """
    Add a period of holiday to the timesheet.
    """
    typer.echo(f"{time_start=} {time_end=} {date=}")

if __name__ == "__main__":
    app()