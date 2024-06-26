import flex_timesheet.common.parse as parse


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
