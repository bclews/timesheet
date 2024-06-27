import pytest
from unittest.mock import patch
from datetime import timedelta, datetime
import typer
import flex_timesheet.common.timesheet as ts

from flex_timesheet.commands.report import (
    report,
    show_entries,
    get_timesheet_data,
    format_hours_and_minutes,
)


@pytest.fixture
def mock_timesheet_data():
    return {
        "standard_working_hours_per_week": {
            "hours": 40,
            "minutes": 0,
            "days_in_working_week": 5,
        },
        "flextime_balance": {"days": 0, "seconds": 0},
        "timesheets": [
            {
                "week_starting": "2023-01-01",
                "work": [
                    {
                        "start": "2023-01-01T09:00:00",
                        "end": "2023-01-01T17:00:00",
                        "location": "Home",
                    },
                ],
                "holiday": [],
                "sick": [],
            }
        ],
    }


@patch("flex_timesheet.common.configuration.get_default_config_path")
@patch("flex_timesheet.common.configuration.read")
@patch("flex_timesheet.common.configuration.get_timesheet_file")
@patch("flex_timesheet.common.timesheet.retrieve_timesheet_file")
def test_get_timesheet_data(
    mock_retrieve, mock_get_file, mock_read, mock_get_path, mock_timesheet_data
):
    mock_get_path.return_value = "config_path"
    mock_read.return_value = {"some": "config"}
    mock_get_file.return_value = "timesheet_file_path"
    mock_retrieve.return_value = mock_timesheet_data

    result = get_timesheet_data()
    assert result == mock_timesheet_data


def test_format_hours_and_minutes():
    result = format_hours_and_minutes(5, 30)
    assert result == "5 hours, 30 minutes"


@patch("flex_timesheet.commands.report.get_timesheet_data")
@patch("typer.echo")
@patch("flex_timesheet.common.calculations.aggregate")
@patch("flex_timesheet.common.calculations.aggregate_timedeltas")
@patch("flex_timesheet.common.calculations.split_timedelta")
@patch("flex_timesheet.common.parse.get_date")
def test_report(
    mock_get_date,
    mock_split,
    mock_aggregate_timedeltas,
    mock_aggregate,
    mock_echo,
    mock_get_timesheet_data,
    mock_timesheet_data,
):
    mock_get_timesheet_data.return_value = mock_timesheet_data
    mock_get_date.return_value = datetime(2023, 1, 1)
    mock_aggregate.return_value = timedelta(hours=8)
    mock_aggregate_timedeltas.return_value = timedelta(hours=8)
    mock_split.side_effect = [
        (8, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (8, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
    ]

    report()

    assert mock_echo.called
    output = "\n".join([call.args[0] for call in mock_echo.call_args_list])
    assert "Week starting: 2023-01-01" in typer.unstyle(output)
    assert "Hours accounted for: 8 hours, 0 minutes" in typer.unstyle(output)
    assert "       accrued flex: 0 hours, 0 minutes" in typer.unstyle(output)
    assert "Total flex: 0 hours, 0 minutes" in typer.unstyle(output)


@patch("flex_timesheet.commands.report.get_timesheet_data")
@patch("typer.echo")
@patch("flex_timesheet.common.parse.get_date")
@patch("flex_timesheet.common.timesheet.get_week_start")
def test_show_entries(
    mock_get_week_start,
    mock_get_date,
    mock_echo,
    mock_get_timesheet_data,
    mock_timesheet_data,
):
    mock_get_timesheet_data.return_value = mock_timesheet_data
    mock_get_week_start.return_value = datetime(2023, 1, 1)
    mock_get_date.return_value = datetime(2023, 1, 1)

    show_entries(datetime(2023, 1, 1))

    assert mock_echo.called
    output = "\n".join([call.args[0] for call in mock_echo.call_args_list])
    assert "Week starting: 2023-01-01" in typer.unstyle(output)
    assert "work from 2023-01-01 09:00 to 2023-01-01 17:00" in typer.unstyle(output)


def test_create_new_timesheet():
    # Given a date, event type, and event log
    the_date = datetime(2022, 1, 1)
    event_type = "work"
    event_log = {"start": "09:00", "end": "17:00"}

    # When we create a new timesheet
    new_timesheet = ts.create_new_timesheet(the_date, event_type, event_log)

    # Then the new timesheet should have the correct structure and data
    assert new_timesheet == {
        "week_starting": "2022-01-01",
        "work": [{"start": "09:00", "end": "17:00"}],
        "holiday": [],
        "sick": [],
    }
