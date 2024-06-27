from flex_timesheet.common import parse
import flex_timesheet.common.configuration as conf
import flex_timesheet.common.timesheet as ts


def add_event(event_type, time_start, time_end, the_date):
    event_log = ts.create_event_log(time_start, time_end, the_date)
    week_start = ts.get_week_start(the_date)

    timesheet_file_path = conf.get_timesheet_file()
    timesheet_file = ts.retrieve_timesheet_file(timesheet_file_path)
    for timesheet in timesheet_file["timesheets"]:
        # find existing timesheets
        if parse.get_date(timesheet["week_starting"]) == week_start:
            timesheet[event_type].append(event_log)
            ts.save_timesheet_file(timesheet_file)
            break
    else:
        # a timesheets does not yet exist for the given date, so create a new one
        timesheet = ts.create_new_timesheet(week_start, event_type, event_log)
        timesheet_file["timesheets"].append(timesheet)
        ts.save_timesheet_file(timesheet_file)
