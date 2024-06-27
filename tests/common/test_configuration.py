import os
from pathlib import Path
import pytest
import tempfile
from flex_timesheet.common import configuration


def test_get_default_config_path():
    config_path = configuration.get_default_config_path()
    assert isinstance(config_path, Path)
    assert str(config_path).endswith(".config/timesheet/timesheet.json")


def test_read_write_config():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    config_path = Path(temp_file.name)
    config_data = {"timesheet_file": "timesheet.json"}

    # Write the configuration data to the file
    configuration.write(config_path, config_data)

    # Read the configuration data from the file
    read_data = configuration.read(config_path)

    assert read_data == config_data

    # Clean up the test configuration file
    os.remove(config_path)


def test_get_timesheet_file(tmp_path):
    # Create a dummy timesheet file
    dummy_file = tmp_path / "timesheet.json"
    dummy_file.touch()

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    config_path = Path(temp_file.name)
    config_data = {"timesheet_file": str(dummy_file)}

    # Write the configuration data to the file
    # configuration.write(config_path, config_data)

    # Get the timesheet file
    timesheet_file = configuration.get_timesheet_file(config_data)

    assert timesheet_file == str(dummy_file)

    # Clean up the test configuration file
    os.remove(config_path)


def test_get_timesheet_file_not_found():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    config_path = Path(temp_file.name)
    # Ensure the configuration file does not exist
    if config_path.exists():
        os.remove(config_path)

    # Attempting to get the timesheet file should raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        configuration.get_timesheet_file({})
