import json
from pathlib import Path


def get_default_config_path():
    """
    Get the default configuration path.
    """
    config_dir = Path.home() / ".config" / "timesheet"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "timesheet.json"


def read(config_path: Path):
    """
    Read the configuration file.
    """
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def write(config_path: Path, config_data: dict):
    """
    Write the configuration file.
    """
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)


def get_timesheet_file():
    """
    Get the timesheet file path. If it does not exist, create it
    with the following content:

    ```json
    {
        "standard_working_hours_per_week": {
            "hours": 36,
            "minutes": 45,
            "days_in_working_week": 5
        },
        "flextime_balance": {
            "days": 0,
            "seconds": 0
        },
        "timesheets": [],
    }
    ```
    """
    config_path = get_default_config_path()
    config_data = read(config_path)

    timesheet_file = config_data.get("timesheet_file", "timesheet.json")
    if not Path(timesheet_file).exists():
        with open(timesheet_file, "w") as f:
            json.dump(
                {
                    "standard_working_hours_per_week": {
                        "hours": 36,
                        "minutes": 45,
                        "days_in_working_week": 5,
                    },
                    "flextime_balance": {"days": 0, "seconds": 0},
                    "timesheets": [],
                },
                f,
                indent=4,
            )

    return timesheet_file
