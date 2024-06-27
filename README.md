# Flex Timesheet

Flex Timesheet is a command-line application for recording and tracking timesheets. It allows you to configure your timesheet settings, add work, sick leave, and holiday periods, and generate reports.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/bclews/timesheet.git
    cd timesheet
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the package:

    ```sh
    pip install .
    ```

## Usage

The application uses the `typer` library to provide a simple and intuitive command-line interface. Below are the available commands and their usage:

### Configure the Application

Configure the timesheet application with a configuration file.

```sh
timesheet configure --config-path /path/to/config/file
```

### Show Configuration

Show the current configuration settings.

```sh
timesheet show_config --config-path /path/to/config/file
```

### Generate Report

Generate a timesheet report to see your work hours and flex time.

```sh
timesheet report
```

### Show Timesheet Entries

Show the timesheet entries for the week of the given date.

```sh
timesheet show_entries 2023-01-01
```

### Add Work Period

Add a period of work to the timesheet.

```sh
timesheet work 09:00 17:00 Home 2023-01-01
```

### Add Sick Leave

Add a period of sick leave to the timesheet.

```sh
timesheet sick 09:00 17:00 2023-01-01
```

### Add Holiday

Add a period of holiday to the timesheet.

```sh
timesheet holiday 09:00 17:00 2023-01-01
```

### Show Timesheets in CSV Format

Print the timesheets to the console in CSV format.

```sh
timesheet show_csv
```

## Timesheet Format

The timesheet is saved as a JSON file, defined in the configuration. The JSON structure of the timesheet is as follows:

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
  "timesheets": [
    {
      "week_starting": "2023-07-03",
      "work": [
        {
          "start": "2023-07-03T09:00:00",
          "end": "2023-07-03T16:21:00",
          "location": "Home"
        },
        {
          "start": "2023-07-04T09:00:00",
          "end": "2023-07-04T16:21:00",
          "location": "Onsite"
        },
        {
          "start": "2023-07-05T09:00:00",
          "end": "2023-07-05T16:21:00",
          "location": "Home"
        },
        {
          "start": "2023-07-06T09:00:00",
          "end": "2023-07-06T16:21:00",
          "location": "Home"
        },
        {
          "start": "2023-07-07T09:00:00",
          "end": "2023-07-07T16:21:00",
          "location": "Home"
        }
      ],
      "holiday": [],
      "sick": []
    }
  ]
}
```

## Commands Overview

- `configure` - Configure the timesheet application.
- `show_config` - Show the current configuration settings.
- `report` - Generate a timesheet report.
- `show_entries` - Show timesheet entries for a specific week.
- `work` - Add a period of work.
- `sick` - Add a period of sick leave.
- `holiday` - Add a period of holiday.
- `show_csv` - Print the timesheets to the console in CSV format.

## Development and Testing

To run the tests, use `pytest`:

```sh
pytest
```

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
