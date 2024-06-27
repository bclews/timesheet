import json
from datetime import datetime
from flex_timesheet.common import timesheet


def test_retrieve_timesheet_file(tmp_path):
    # Given a timesheet file with some data
    timesheet_file = tmp_path / "timesheet.json"
    timesheet_data = {"key": "value"}
    timesheet_file.write_text(json.dumps(timesheet_data))

    # When we retrieve the timesheet file
    retrieved_data = timesheet.retrieve_timesheet_file(timesheet_file)

    # Then the data that was retrieved should be the same as the data in the file
    assert retrieved_data == timesheet_data


def test_save_timesheet_file(tmp_path):
    # Given a timesheet file and some data
    timesheet_file = tmp_path / "timesheet.json"
    timesheet_data = {
        "standard_working_hours_per_week": 40,
        "flextime_balance": 0,
        "timesheets": [],
    }

    # When we save the data to the timesheet file
    timesheet.save_timesheet_file(timesheet_file, timesheet_data)

    # Then the data in the timesheet file should be the same as the data that was saved
    saved_data = json.loads(timesheet_file.read_text())
    assert saved_data == timesheet_data


def test_sort_timesheets():
    # Given some unsorted timesheets
    timesheets = {
        "standard_working_hours_per_week": 40,
        "flextime_balance": 0,
        "timesheets": [
            {
                "week_starting": "2022-01-10",
                "work": [],
                "holiday": [],
                "sick": [],
            },
            {
                "week_starting": "2022-01-03",
                "work": [],
                "holiday": [],
                "sick": [],
            },
        ],
    }

    # When we sort the timesheets
    sorted_timesheets = timesheet.sort(timesheets)

    # Then the timesheets should be sorted by week_starting
    assert sorted_timesheets["timesheets"] == [
        {
            "week_starting": "2022-01-03",
            "work": [],
            "holiday": [],
            "sick": [],
        },
        {
            "week_starting": "2022-01-10",
            "work": [],
            "holiday": [],
            "sick": [],
        },
    ]


def test_create_new_timesheet():
    # Given a date, event type, and event log
    the_date = datetime(2022, 1, 1)
    event_type = "work"
    event_log = {"start": "09:00", "end": "17:00"}

    # When we create a new timesheet
    new_timesheet = timesheet.create_new_timesheet(the_date, event_type, event_log)

    # Then the new timesheet should have the correct structure and data
    assert new_timesheet == {
        "week_starting": "2022-01-01",
        "work": [{"start": "09:00", "end": "17:00"}],
        "holiday": [],
        "sick": [],
    }


def test_get_week_start():
    # Given a date that is not a Monday
    the_date = "2022-01-05"  # This is a Wednesday

    # When we get the start of the week for this date
    week_start = timesheet.get_week_start(the_date)

    # Then the start of the week should be the previous Monday
    assert week_start == datetime(2022, 1, 3)


def test_create_event_log():
    # Given a start time, end time, and date
    time_start = "09:00"
    time_end = "17:00"
    the_date = "2022-01-01"

    # When we create an event log
    event_log = timesheet.create_event_log(time_start, time_end, the_date)

    # Then the event log should have the correct structure and data
    assert event_log == {
        "start": "2022-01-01T09:00:00",
        "end": "2022-01-01T17:00:00",
    }
