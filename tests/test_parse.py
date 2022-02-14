from flex_timesheet import parse

#
# Testing `invalid_time`
#
def test_random_string_is_not_a_valid_time():
    assert parse.invalid_time("abcd") == True


def test_minus_1_oclock_is_not_a_valid_time():
    assert parse.invalid_time("-0:00") == True


def test_0_oclock_is_a_valid_time():
    assert parse.invalid_time("0:00") == False


def test_23_hours_59_minutes_is_a_valid_time():
    assert parse.invalid_time("23:59") == False


def test_24_oclock_is_not_a_valid_time():
    assert parse.invalid_time("24:00") == True


def test_seconds_is_not_wanted_either():
    assert parse.invalid_time("23:00:11") == True


def test_12_hour_format_is_not_wanted_also():
    assert parse.invalid_time("08:00 am") == True


#
# Testing `invalid_datepy`
#
