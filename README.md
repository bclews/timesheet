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

## Commands Overview

- `configure` - Configure the timesheet application.
- `show_config` - Show the current configuration settings.
- `report` - Generate a timesheet report.
- `show_entries` - Show timesheet entries for a specific week.
- `work` - Add a period of work.
- `sick` - Add a period of sick leave.
- `holiday` - Add a period of holiday.

## Development and Testing

To run the tests, use `pytest`:

```sh
pytest
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

```

This README.md now includes instructions on how to install and use the CLI application based on your `setup.py` file. Adjust any additional details as necessary.
