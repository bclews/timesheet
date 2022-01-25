import pytest
from datetime import datetime, timedelta
from flex_timesheet import calculations

def test_split_timedelta_none():
    # setup
    duration = None
    
    # test
    hours, minutes, seconds = calculations.split_timedelta(duration)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0

def test_split_timedelta_passing_in_wrong_type():
    # setup
    duration = "THIS_IS_A_DAMN_STRING"
    
    # test
    hours, minutes, seconds = calculations.split_timedelta(duration)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0

def test_split_timedelta_zero():
    # setup
    duration = timedelta()
    
    # test
    hours, minutes, seconds = calculations.split_timedelta(duration)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0

def test_split_timedelta():
    # setup
    duration = timedelta(hours=2, seconds=2705)
    
    # test
    hours, minutes, seconds = calculations.split_timedelta(duration)
    assert hours == 2
    assert minutes == 45
    assert seconds == 5

def test_aggregate_none():
    # setup
    periods = None

    #test
    hours, minutes, seconds = calculations.aggregate(periods)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0    

def test_aggregate_zero():
    # setup
    periods = []

    #test
    hours, minutes, seconds = calculations.aggregate(periods)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0    

def test_aggregate():
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
        {"start": "2022-01-14T13:00", "end": "2022-01-14T16:40"}
    ]

    #test
    hours, minutes, seconds = calculations.aggregate(periods)
    assert hours == 38
    assert minutes == 20
    assert seconds == 0    

def test_aggregate_with_incorrect_dictionary_keys():
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
        {"from": "2022-01-14T13:00", "to": "2022-01-14T16:40"}
    ]

    #test
    hours, minutes, seconds = calculations.aggregate(periods)
    assert hours == 0
    assert minutes == 0
    assert seconds == 0    