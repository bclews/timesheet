import pytest
import timesheet.common.parse as parse
from timesheet.common.parse import InputException


#
# Testing `invalid_time`
#
def test_random_string_is_not_a_valid_time():
    assert parse.invalid_time("abcd")


def test_minus_1_oclock_is_not_a_valid_time():
    assert parse.invalid_time("-0:00")


def test_0_oclock_is_a_valid_time():
    assert not parse.invalid_time("0:00")


def test_23_hours_59_minutes_is_a_valid_time():
    assert not parse.invalid_time("23:59")


def test_24_oclock_is_not_a_valid_time():
    assert parse.invalid_time("24:00")


def test_seconds_is_not_wanted_either():
    assert parse.invalid_time("23:00:11")


def test_12_hour_format_is_not_wanted_also():
    assert parse.invalid_time("08:00 am")


#
# Testing `invalid_date`
#
def test_random_strings_are_not_a_valid_date():
    assert parse.invalid_date("abcd")


def test_formats_are_invalid():
    assert parse.invalid_date("22-12-01")
    assert parse.invalid_date("01-12-22")
    assert parse.invalid_date("01-12-2022")


def test_bunch_of_invalid_dates():
    assert parse.invalid_date("2022-01-32")
    assert parse.invalid_date("2022-02-32")
    assert parse.invalid_date("2022-03-32")
    assert parse.invalid_date("2022-04-32")
    assert parse.invalid_date("2022-05-32")
    assert parse.invalid_date("2022-06-32")
    assert parse.invalid_date("2022-07-32")
    assert parse.invalid_date("2022-08-32")
    assert parse.invalid_date("2022-09-32")
    assert parse.invalid_date("2022-10-32")
    assert parse.invalid_date("2022-11-32")
    assert parse.invalid_date("2022-12-32")


def test_bunch_of_valid_dates():
    assert not parse.invalid_date("2022-01-01")
    assert not parse.invalid_date("2022-02-01")
    assert not parse.invalid_date("2022-03-01")
    assert not parse.invalid_date("2022-04-01")
    assert not parse.invalid_date("2022-05-01")
    assert not parse.invalid_date("2022-06-01")
    assert not parse.invalid_date("2022-07-01")
    assert not parse.invalid_date("2022-08-01")
    assert not parse.invalid_date("2022-09-01")
    assert not parse.invalid_date("2022-10-01")
    assert not parse.invalid_date("2022-11-01")
    assert not parse.invalid_date("2022-12-01")


def test_get_datetime():
    # Given a valid date and time
    the_date = "2022-01-01"
    the_time = "09:00"

    # When we get the datetime
    the_datetime = parse.get_datetime(the_date, the_time)

    # Then the datetime should be correct
    assert the_datetime == parse.datetime(2022, 1, 1, 9, 0)


def test_get_datetime_invalid_date():
    # Given an invalid date and a valid time
    the_date = "invalid"
    the_time = "09:00"

    # When we try to get the datetime
    # Then an InputException should be raised
    with pytest.raises(InputException):
        parse.get_datetime(the_date, the_time)


def test_get_datetime_invalid_time():
    # Given a valid date and an invalid time
    the_date = "2022-01-01"
    the_time = "invalid"

    # When we try to get the datetime
    # Then an InputException should be raised
    with pytest.raises(InputException):
        parse.get_datetime(the_date, the_time)


def test_get_date():
    # Given a valid date
    the_date = "2022-01-01"

    # When we get the date
    date = parse.get_date(the_date)

    # Then the date should be correct
    assert date == parse.datetime(2022, 1, 1)


def test_get_date_invalid():
    # Given an invalid date
    the_date = "invalid"

    # When we try to get the date
    # Then an InputException should be raised
    with pytest.raises(InputException):
        parse.get_date(the_date)
