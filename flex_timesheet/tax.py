import json
from datetime import datetime
import csv

# Load JSON data
with open('flex_timesheet.json') as f:
    data = json.load(f)

# Extract work items
work_items = [dict(item, week_starting=timesheet['week_starting']) for timesheet in data['timesheets'] for item in timesheet['work']]

# Calculate hours
for item in work_items:
    start = datetime.fromisoformat(item['start'])
    end = datetime.fromisoformat(item['end'])
    item['hours'] = (end - start).seconds / 3600

# Write to CSV
with open('flex_timesheet_tax.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['week_starting', 'start', 'end', 'hours', 'location'])
    writer.writeheader()
    writer.writerows(work_items)
