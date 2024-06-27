from datetime import date, timedelta

import flex_timesheet.common.calculations as calculations
import pytest


#
# Testing `split_timedelta`
#
def test_duration_is_none():
    # setup
    duration = None

    # test
    hours, minutes, seconds = calculations.split_timedelta(duration)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0


def test_duration_is_wrong_type():
    # setup
    duration = "THIS_IS_A_DAMN_STRING"

    # test
    hours, minutes, seconds = calculations.split_timedelta(duration)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0


def test_duration_is_zero():
    # setup
    duration = timedelta()

    # test
    hours, minutes, seconds = calculations.split_timedelta(duration)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0


def test_duration_is_a_valid_value():
    # setup
    duration = timedelta(hours=2, seconds=2705)

    # test
    hours, minutes, seconds = calculations.split_timedelta(duration)
    assert hours == 2
    assert minutes == 45
    assert seconds == 5


#
# Testing `aggregate`
#
def test_periods_is_none():
    # setup
    periods = None

    # test
    aggregate = calculations.aggregate(periods)
    hours, minutes, seconds = calculations.split_timedelta(aggregate)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0


def test_periods_is_zero():
    # setup
    periods = []

    # test
    aggregate = calculations.aggregate(periods)
    hours, minutes, seconds = calculations.split_timedelta(aggregate)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0


def test_periods_is_valid_value():
    # setup
    periods = [
        {"start": "2022-01-10T08:00", "end": "2022-01-10T12:00"},
        {"start": "2022-01-10T13:00", "end": "2022-01-10T16:40"},
        {"start": "2022-01-11T08:00", "end": "2022-01-11T12:00"},
        {"start": "2022-01-11T13:00", "end": "2022-01-11T16:40"},
        {"start": "2022-01-12T08:00", "end": "2022-01-12T12:00"},
        {"start": "2022-01-12T13:00", "end": "2022-01-12T16:40"},
        {"start": "2022-01-13T08:00", "end": "2022-01-13T12:00"},
        {"start": "2022-01-13T13:00", "end": "2022-01-13T16:40"},
        {"start": "2022-01-14T08:00", "end": "2022-01-14T12:00"},
        {"start": "2022-01-14T13:00", "end": "2022-01-14T16:40"},
    ]

    # test
    aggregate = calculations.aggregate(periods)
    hours, minutes, seconds = calculations.split_timedelta(aggregate)
    assert hours == 38
    assert minutes == 20
    assert seconds == 0


def test_test_periods_is_a_dcitionary_with_incorrect_keys():
    # setup
    periods = [
        {"from": "2022-01-10T08:00", "to": "2022-01-10T12:00"},
        {"from": "2022-01-10T13:00", "to": "2022-01-10T16:40"},
        {"from": "2022-01-11T08:00", "to": "2022-01-11T12:00"},
        {"from": "2022-01-11T13:00", "to": "2022-01-11T16:40"},
        {"from": "2022-01-12T08:00", "to": "2022-01-12T12:00"},
        {"from": "2022-01-12T13:00", "to": "2022-01-12T16:40"},
        {"from": "2022-01-13T08:00", "to": "2022-01-13T12:00"},
        {"from": "2022-01-13T13:00", "to": "2022-01-13T16:40"},
        {"from": "2022-01-14T08:00", "to": "2022-01-14T12:00"},
        {"from": "2022-01-14T13:00", "to": "2022-01-14T16:40"},
    ]

    # test
    aggregate = calculations.aggregate(periods)
    hours, minutes, seconds = calculations.split_timedelta(aggregate)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0


#
# Testing `find_date_of_previous_monday`
#
def test_get_previous_monday_if_date_is_a_wednesday():
    # setup: Wednesday 9th Febraury 2022
    given_date = date(year=2022, month=2, day=9)
    expected_date = date(year=2022, month=2, day=7)

    # test
    last_monday = calculations.find_date_of_previous_monday(given_date)
    assert expected_date == last_monday


def test_get_previous_monday_if_date_is_a_monday():
    # setup: Monday 7th Febraury 2022
    given_date = date(year=2022, month=2, day=7)
    expected_date = date(year=2022, month=2, day=7)

    # test
    last_monday = calculations.find_date_of_previous_monday(given_date)
    assert expected_date == last_monday


def test_get_previous_monday_if_date_is_None():
    with pytest.raises(
        TypeError, match="`given_date` should be a date type, not <class 'NoneType'>"
    ):
        assert calculations.find_date_of_previous_monday(None)


def test_get_previous_monday_if_date_is_wrong_type():
    with pytest.raises(
        TypeError, match="`given_date` should be a date type, not <class 'str'>"
    ):
        assert calculations.find_date_of_previous_monday("THIS_IS_A_DAMN_STRING")


#
# Testing `find_date_of_next_monday`
#
def test_get_next_monday_if_date_is_a_wednesday():
    # setup: Wednesday 9th Febraury 2022
    given_date = date(year=2022, month=2, day=9)
    expected_date = date(year=2022, month=2, day=14)

    # test
    last_monday = calculations.find_date_of_next_monday(given_date)
    assert expected_date == last_monday


def test_get_next_monday_if_date_is_a_monday():
    # setup: Monday 7th Febraury 2022
    given_date = date(year=2022, month=2, day=7)
    expected_date = date(year=2022, month=2, day=14)

    # test
    last_monday = calculations.find_date_of_next_monday(given_date)
    assert expected_date == last_monday


def test_get_next_monday_if_date_is_None():
    with pytest.raises(
        TypeError, match="`given_date` should be a date type, not <class 'NoneType'>"
    ):
        assert calculations.find_date_of_next_monday(None)


def test_get_next_monday_if_date_is_wrong_type():
    with pytest.raises(
        TypeError, match="`given_date` should be a date type, not <class 'str'>"
    ):
        assert calculations.find_date_of_next_monday("THIS_IS_A_DAMN_STRING")


#
# Testing `is_timedelta_positive`
#
def test_with_positive_timedelta():
    delta = timedelta(days=1)
    assert calculations.is_timedelta_positive(delta)


def test_with_negative_timedelta():
    delta = timedelta(days=-1)
    assert not calculations.is_timedelta_positive(delta)


def test_with_zero_timedelta():
    delta = timedelta(days=0)
    assert calculations.is_timedelta_positive(delta)


def test_with_date_being_None():
    with pytest.raises(
        TypeError, match="`delta` should be a date type, not <class 'NoneType'>"
    ):
        assert calculations.is_timedelta_positive(None)


#
# Testing `aggregate_timedeltas`
#
def test_aggregate_timedeltas():
    # Given a list of timedeltas
    timedeltas = [timedelta(hours=1), timedelta(hours=2), timedelta(hours=3)]

    # When we aggregate the timedeltas
    total_timedelta = calculations.aggregate_timedeltas(timedeltas)

    # Then the total timedelta should be the sum of the timedeltas
    assert total_timedelta == timedelta(hours=6)
