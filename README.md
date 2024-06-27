# Flex Timesheet

Flex Timesheet is a command-line application for recording and tracking timesheets. It allows you to configure your timesheet settings, add work, sick leave, and holiday periods, and generate reports.

I initially created this application to help me keep track of my work hours and flex time. I wanted a simple and easy-to-use tool that would allow me to record my work hours and generate reports to see how many hours I had worked and how much flex time I had accumulated.

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

### JSON Schema Explanation

This JSON schema is designed to track timesheets, including working hours, flextime balance, and various types of leave (holiday and sick leave). Below is a detailed explanation of each part of the schema:

#### Root Object

The root object contains three main properties:

1. `standard_working_hours_per_week`
2. `flextime_balance`
3. `timesheets`

#### `standard_working_hours_per_week`

This object defines the standard working hours for a week. It has three properties:

- `hours`: The total number of hours expected to be worked in a week. In this case, it is set to 36 hours.
- `minutes`: Additional minutes to be worked in a week. Here, it is set to 45 minutes.
- `days_in_working_week`: The number of working days in a week. Here, it is set to 5 days.

These standard working hours are used to calculate flextime by comparing them against the actual hours worked in a week.

#### `flextime_balance`

This object tracks the initial balance of flextime (flexible working hours) brought forward from a previous timesheet. It has two properties:

- `days`: The number of days of flextime balance. Initially set to 0.
- `seconds`: The number of seconds of flextime balance. Initially set to 0.

The `flextime_balance` is used in conjunction with the actual hours worked and the `standard_working_hours_per_week` to calculate the new flextime balance.

#### `timesheets`

This is an array of timesheet entries, where each entry corresponds to a specific week. Each entry in the `timesheets` array is an object with the following properties:

##### `week_starting`

A string representing the starting date of the week in `YYYY-MM-DD` format. For example, "2023-07-03" indicates the week starting on July 3, 2023.

##### `work`

This is an array of work periods within the week. Each work period is an object with the following properties:

- `start`: A string representing the start date and time of the work period in ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`). For example, "2023-07-03T09:00:00" indicates the work period starts on July 3, 2023, at 9:00 AM.
- `end`: A string representing the end date and time of the work period in ISO 8601 format. For example, "2023-07-03T16:21:00" indicates the work period ends on July 3, 2023, at 4:21 PM.
- `location`: A string indicating the location where the work was performed. For example, "Home" or "Onsite".

##### `holiday`

This is an array of holiday periods within the week. Each holiday period is an object but is empty in the given schema, indicating no holidays were taken in the example week.

##### `sick`

This is an array of sick leave periods within the week. Each sick leave period is an object but is empty in the given schema, indicating no sick leave was taken in the example week.

### Flextime Calculation

The flextime calculation involves the following steps:

1. Determine the total actual hours worked in the week by summing up the durations of all work periods.
2. Compare the total actual hours worked with the standard working hours for the week (defined in `standard_working_hours_per_week`).
3. Adjust the `flextime_balance` based on the difference between the actual hours worked and the standard working hours:
   - If actual hours worked exceed the standard working hours, the excess is added to the `flextime_balance`.
   - If actual hours worked are less than the standard working hours, the deficit is subtracted from the `flextime_balance`.

### Example Breakdown

Given the example JSON schema:

- The standard working hours per week are 36 hours and 45 minutes across 5 days.
- The initial flextime balance is 0 days and 0 seconds.
- For the week starting on July 3, 2023, there are five work periods logged:
  - On July 3, 2023, work from 9:00 AM to 4:21 PM at "Home".
  - On July 4, 2023, work from 9:00 AM to 4:21 PM at "Onsite".
  - On July 5, 2023, work from 9:00 AM to 4:21 PM at "Home".
  - On July 6, 2023, work from 9:00 AM to 4:21 PM at "Home".
  - On July 7, 2023, work from 9:00 AM to 4:21 PM at "Home".
- No holiday or sick leave periods are recorded for this week.

By calculating the actual hours worked and comparing them to the standard working hours, the new flextime balance is determined and carried over to the next timesheet.

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
