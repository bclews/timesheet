import pytest
from unittest.mock import patch
from datetime import datetime

from timesheet.commands.timesheet import add_event

# Mock data
mock_event_log = {"start": "09:00", "end": "17:00", "date": "2024-06-27"}

mock_timesheet_file = {"timesheets": [{"week_starting": "2024-06-24", "work": []}]}


@pytest.fixture
def mock_event_type():
    return "work"


@pytest.fixture
def mock_time_start():
    return "09:00"


@pytest.fixture
def mock_time_end():
    return "17:00"


@pytest.fixture
def mock_the_date():
    return datetime.strptime("2024-06-27", "%Y-%m-%d")


@pytest.fixture
def mock_get_location():
    return "Office"


@patch("timesheet.common.timesheet.save_timesheet_file")
@patch("timesheet.common.timesheet.retrieve_timesheet_file")
@patch("timesheet.common.timesheet.create_event_log")
@patch("timesheet.common.timesheet.get_week_start")
@patch("timesheet.common.configuration.get_timesheet_file")
@patch("timesheet.common.parse.get_date")
def test_add_event_existing_timesheet(
    mock_get_date,
    mock_get_timesheet_file,
    mock_get_week_start,
    mock_create_event_log,
    mock_retrieve_timesheet_file,
    mock_save_timesheet_file,
    mock_event_type,
    mock_time_start,
    mock_time_end,
    mock_the_date,
    mock_get_location,
):
    # Arrange
    mock_get_date.return_value = datetime.strptime("2024-06-24", "%Y-%m-%d")
    mock_get_week_start.return_value = datetime.strptime("2024-06-24", "%Y-%m-%d")
    mock_create_event_log.return_value = mock_event_log
    mock_get_timesheet_file.return_value = "/mock/timesheet/file/path"
    mock_retrieve_timesheet_file.return_value = mock_timesheet_file

    # Act
    add_event(
        mock_event_type,
        mock_time_start,
        mock_time_end,
        mock_the_date,
        mock_get_location,
    )

    # Assert
    mock_create_event_log.assert_called_once_with(
        mock_time_start, mock_time_end, mock_the_date, mock_get_location
    )
    mock_get_week_start.assert_called_once_with(mock_the_date)
    mock_retrieve_timesheet_file.assert_called_once_with("/mock/timesheet/file/path")
    mock_get_date.assert_called_once_with("2024-06-24")
    assert mock_event_log in mock_timesheet_file["timesheets"][0][mock_event_type]
    mock_save_timesheet_file.assert_called_once_with(
        "/mock/timesheet/file/path", mock_timesheet_file
    )


@patch("timesheet.common.timesheet.save_timesheet_file")
@patch("timesheet.common.timesheet.retrieve_timesheet_file")
@patch("timesheet.common.timesheet.create_event_log")
@patch("timesheet.common.timesheet.create_new_timesheet")
@patch("timesheet.common.timesheet.get_week_start")
@patch("timesheet.common.configuration.get_timesheet_file")
def test_add_event_new_timesheet(
    mock_get_timesheet_file,
    mock_get_week_start,
    mock_create_new_timesheet,
    mock_create_event_log,
    mock_retrieve_timesheet_file,
    mock_save_timesheet_file,
    mock_event_type,
    mock_time_start,
    mock_time_end,
    mock_the_date,
    mock_get_location,
):
    # Arrange
    mock_get_week_start.return_value = datetime.strptime("2024-06-24", "%Y-%m-%d")
    mock_create_event_log.return_value = mock_event_log
    mock_get_timesheet_file.return_value = "/mock/timesheet/file/path"
    mock_retrieve_timesheet_file.return_value = {"timesheets": []}
    mock_new_timesheet = {
        "week_starting": "2024-06-24",
        mock_event_type: [mock_event_log],
    }
    mock_create_new_timesheet.return_value = mock_new_timesheet

    # Act
    add_event(
        mock_event_type,
        mock_time_start,
        mock_time_end,
        mock_the_date,
        mock_get_location,
    )

    # Assert
    mock_create_event_log.assert_called_once_with(
        mock_time_start, mock_time_end, mock_the_date, mock_get_location
    )
    mock_get_week_start.assert_called_once_with(mock_the_date)
    mock_retrieve_timesheet_file.assert_called_once_with("/mock/timesheet/file/path")
    mock_create_new_timesheet.assert_called_once_with(
        mock_get_week_start.return_value, mock_event_type, mock_event_log
    )
    assert mock_new_timesheet in mock_retrieve_timesheet_file.return_value["timesheets"]
    mock_save_timesheet_file.assert_called_once_with(
        "/mock/timesheet/file/path", mock_retrieve_timesheet_file.return_value
    )
