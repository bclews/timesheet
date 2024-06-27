import csv
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import call, patch

import timesheet.common.timesheet as ts
import pytest
import typer
from timesheet.commands.report import (
    EchoWriter,
    format_hours_and_minutes,
    get_timesheet_data,
    report,
    show_csv,
    show_entries,
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
            },
            {
                "week_starting": "2023-01-08",
                "work": [
                    {
                        "start": "2023-01-08T08:00:00",
                        "end": "2023-01-08T16:00:00",
                        "location": "Office",
                    },
                ],
                "holiday": [],
                "sick": [
                    {
                        "start": "2023-01-09T00:00:00",
                        "end": "2023-01-09T23:59:59",
                    },
                ],
            },
        ],
    }


@patch("timesheet.common.configuration.get_default_config_path")
@patch("timesheet.common.configuration.read")
@patch("timesheet.common.configuration.get_timesheet_file")
@patch("timesheet.common.timesheet.retrieve_timesheet_file")
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


@patch("timesheet.commands.report.get_timesheet_data")
@patch("typer.echo")
@patch("timesheet.common.calculations.aggregate")
@patch("timesheet.common.calculations.aggregate_timedeltas")
@patch("timesheet.common.calculations.split_timedelta")
@patch("timesheet.common.parse.get_date")
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

    def mock_split_side_effect(*args):
        if args[0] == mock_aggregate_timedeltas.return_value:
            return (0, 0, 0)
        return (8, 0, 0)

    mock_split.side_effect = mock_split_side_effect

    report()

    assert mock_echo.called
    output = "\n".join([call.args[0] for call in mock_echo.call_args_list])
    print(output)  # Add this line to inspect the actual output during the test
    assert "Week starting: 2023-01-01" in typer.unstyle(output)
    assert "Hours accounted for: 0 hours, 0 minutes" in typer.unstyle(output)
    assert "               work: 0 hours, 0 minutes" in typer.unstyle(output)
    assert "            holiday: 0 hours, 0 minutes" in typer.unstyle(output)
    assert "               sick: 0 hours, 0 minutes" in typer.unstyle(output)
    assert "       accrued flex: 8 hours, 0 minutes" in typer.unstyle(output)
    assert "Total flex: 8 hours, 0 minutes" in typer.unstyle(output)


@patch("timesheet.commands.report.get_timesheet_data")
@patch("typer.echo")
@patch("timesheet.common.parse.get_date")
@patch("timesheet.common.timesheet.get_week_start")
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


@patch("timesheet.commands.report.get_timesheet_data")
@patch("typer.echo")
def test_show_csv(mock_echo, mock_get_timesheet_data, mock_timesheet_data):
    mock_get_timesheet_data.return_value = mock_timesheet_data

    show_csv()

    # Check that typer.echo was called with the correct CSV data
    expected_calls = [
        call("week_starting,event_type,start,end,location\r\n", nl=False),
        call(
            "2023-01-01,work,2023-01-01T09:00:00,2023-01-01T17:00:00,Home\r\n", nl=False
        ),
        call(
            "2023-01-08,work,2023-01-08T08:00:00,2023-01-08T16:00:00,Office\r\n",
            nl=False,
        ),
        call("2023-01-08,sick,2023-01-09T00:00:00,2023-01-09T23:59:59,\r\n", nl=False),
    ]
    mock_echo.assert_has_calls(expected_calls, any_order=False)


@patch("timesheet.commands.report.get_timesheet_data")
def test_show_csv_output_format(mock_get_timesheet_data, mock_timesheet_data):
    mock_get_timesheet_data.return_value = mock_timesheet_data

    # Capture the output
    output = StringIO()
    with patch("sys.stdout", output):
        show_csv()

    # Reset the StringIO cursor
    output.seek(0)

    # Read the CSV output
    csv_reader = csv.DictReader(output)
    rows = list(csv_reader)

    # Check the number of rows and their content
    assert len(rows) == 3
    assert rows[0] == {
        "week_starting": "2023-01-01",
        "event_type": "work",
        "start": "2023-01-01T09:00:00",
        "end": "2023-01-01T17:00:00",
        "location": "Home",
    }
    assert rows[1] == {
        "week_starting": "2023-01-08",
        "event_type": "work",
        "start": "2023-01-08T08:00:00",
        "end": "2023-01-08T16:00:00",
        "location": "Office",
    }
    assert rows[2] == {
        "week_starting": "2023-01-08",
        "event_type": "sick",
        "start": "2023-01-09T00:00:00",
        "end": "2023-01-09T23:59:59",
        "location": "",
    }


def test_echo_writer():
    writer = EchoWriter()

    with patch("typer.echo") as mock_echo:
        writer.write("Test message")
        writer.flush()

    mock_echo.assert_called_once_with("Test message", nl=False)
