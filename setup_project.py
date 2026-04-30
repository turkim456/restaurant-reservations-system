import csv
import json
import os
from datetime import datetime,timedelta


available_times = ["7:00", "7:30", "8:00", "8:30", "9:00",
                   "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30"]
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]






today_str = datetime.now().strftime("%Y-%m-%d")
date_file = "last_update.txt"

already_updated = False
if os.path.exists(date_file):
    with open(date_file, "r") as f:
        if f.read().strip() == today_str:
            already_updated = True
            print("it already update ")




if not already_updated:
    # 1. Update the Schedule
    schedule = {}
    today = datetime.now()
    for i in range(7):
        target_date = today + timedelta(days=i)
        date_key = target_date.strftime("%Y-%m-%d (%A)")
        schedule[date_key] = list(available_times)

    with open("schedule.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["day", "time"])
        writer.writeheader()
        for d, t in schedule.items():
            writer.writerow({"day": d, "time": json.dumps(t)})

    
    with open(date_file, "w") as f:
        f.write(today_str)

    print("Daily cleanup finished: The 7-day schedule has been updated.")

    
    if os.path.exists("confirmed.csv"):
        temp_rows = []
        today_date_cmp = datetime.now().strftime("%Y-%m-%d")

        with open("confirmed.csv", "r") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                booking_date = row['day'][:10]
                if booking_date >= today_date_cmp:
                    temp_rows.append(row)

        with open("confirmed.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(temp_rows)

        print("Cleanup finished: Old history removed.")
