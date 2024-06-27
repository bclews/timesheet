import pytest
from unittest.mock import patch
from pathlib import Path

import flex_timesheet.commands.configuration as conf

# Mock data
mock_config_data = {"timesheet_file": "~/timesheet.json"}


@pytest.fixture
def mock_config_path():
    return Path("/mock/config/path")


@patch("flex_timesheet.common.configuration.read")
@patch("flex_timesheet.common.configuration.write")
@patch("typer.prompt")
@patch("os.path.expanduser")
def test_configure(
    mock_expanduser, mock_prompt, mock_write, mock_read, mock_config_path
):
    # Arrange
    mock_read.return_value = mock_config_data
    mock_prompt.return_value = "~/new_timesheet.json"
    mock_expanduser.return_value = "/home/user/new_timesheet.json"

    # Act
    conf.configure(mock_config_path)

    # Assert
    mock_read.assert_called_once_with(mock_config_path)
    mock_prompt.assert_called_once_with(
        "Enter the location to save your timesheet", default="~/timesheet.json"
    )
    mock_expanduser.assert_called_once_with("~/new_timesheet.json")
    expected_config_data = mock_config_data.copy()
    expected_config_data["timesheet_file"] = "/home/user/new_timesheet.json"
    mock_write.assert_called_once_with(mock_config_path, expected_config_data)


@patch("flex_timesheet.common.configuration.read")
def test_show_config(mock_read, mock_config_path):
    # Arrange
    mock_read.return_value = mock_config_data

    # Act
    conf.show_config(mock_config_path)

    # Assert
    mock_read.assert_called_once_with(mock_config_path)
