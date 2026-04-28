import csv
import json
import sys
from datetime import datetime
import os


available_times = ["7:00", "7:30", "8:00", "8:30", "9:00",
                   "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30"]
days_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

schedule = {}
try:
    with open("schedule.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            schedule[row['day']] = json.loads(row['time'])
except FileNotFoundError:
    print("Error: schedule.csv not found. Please create the file first.")
    sys.exit()


def menu():
    print("\nWelcome to our Restaurant")
    print("------------------------------------------")
    print("What service do you want? Choice number:")
    print("1- New Book")
    print("2- Show Book")
    print("3- Cancel Book")
    print("4- Exit")


def Vaild_number():
    # menu_numbers = ["1", "2", "3", "4"]

    while True:
        menu()  # Show main menu
        user_input = input("Choose a service (1-4): ").strip()

        if user_input == "1":
            saved_name = new_booking()
            if saved_name:
                print(f"\nBooking for {saved_name} is done!")
                next_step = input(
                    "Press 2 to SHOW details, 0 to EXIT, or any key for MAIN MENU: ").strip()

                if next_step == "2":
                    show_booking(saved_name)
                    input("\nPress Enter to go to Main Menu...")
                elif next_step == "0":
                    print("Bye Bye")
                    sys.exit()

        elif user_input == "2":
            show_booking()
            next_step = input("\nBooking shown. Press 0 to EXIT or any key for MAIN MENU: ").strip()
            if next_step == "0":
                sys.exit()

        elif user_input == "3":
            cancel_booking()
            input("\nCanceled. Press Enter to return to Main Menu...")

        elif user_input == "4":
            print("Bye Bye")
            sys.exit()

        else:

            os.system('cls' if os.name == 'nt' else 'clear')
            menu()
            print("\n Please enter a valid number (0-4)")

            user_input = input("Choose a number: ").strip()


def new_booking():
    global schedule

    dates_list = list(schedule.keys())
    for i, date_label in enumerate(dates_list):
        print(f"{i} - {date_label}")

    while True:
        choice = input("Select date number: ")
        if choice.isdigit() and 0 <= int(choice) < len(dates_list):
            chosen_day = dates_list[int(choice)]
            break

    valid_time = True
    while valid_time:
        if not schedule[chosen_day]:
            print("All times full for this day!")
            return None

        print(f"Available times for {chosen_day}: {schedule[chosen_day]}")
        chosen_time = input("Choose time from above: ")

        if chosen_time in schedule[chosen_day]:
            while True:
                fname = input("Enter your First Name: ").strip().capitalize()
                if fname.isalpha() and len(fname) >= 3:
                    break
                print("Invalid name. Please use at least 3 letters.")

            while True:
                lname = input("Enter your Last Name: ").strip().capitalize()
                if lname.isalpha() and len(lname) >= 2:
                    break
                print("Invalid name. Please use letters only.")

            while True:
                phone = input("Enter your 10-digit Phone Number: ").strip()
                if phone.isdigit() and len(phone) == 10:
                    break
                print("Invalid phone. Must be exactly 10 digits.")

            full_name = f"{fname} {lname}"
            valid_time = False
        else:
            print("Please enter a valid time from the list.")

    file_name = "confirmed.csv"
    file_is_there = os.path.exists(file_name)
    with open(file_name, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["full_name", "phone", "day", "time"])
        if not file_is_there:
            writer.writeheader()
        writer.writerow({
            "full_name": full_name,
            "phone": phone,
            "day": chosen_day,
            "time": chosen_time
        })

    schedule[chosen_day].remove(chosen_time)
    with open("schedule.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["day", "time"])
        writer.writeheader()
        for d_key, t_list in schedule.items():
            writer.writerow({"day": d_key, "time": json.dumps(t_list)})

    print(f"\nBooking confirmed for {full_name}!")
    return full_name


def show_booking(saved_name=None):
    if saved_name is None:
        saved_name = input("Enter your Firstname and Lastname to search: ").strip()
    found = False

    if os.path.exists("confirmed.csv"):
        with open("confirmed.csv", "r") as f:
            reader = csv.DictReader(f)
            for line in reader:
                if line['full_name'].lower() == saved_name.strip().lower():
                    print("\nBooking found:")
                    print(f"Name : {line['full_name']}")
                    print(f"Phone: {line['phone']}")
                    print(f"Day  : {line['day']}")
                    print(f"Time : {line['time']}")
                    print("----------------------")
                    found = True

    if not found:
        print("No booking found with this name.")


def cancel_booking():
    global schedule
    name_to_cancel = input("Enter your name to delete your booking: ").strip().lower()

    if os.path.exists("confirmed.csv"):
        with open("confirmed.csv", "r") as f:

            rows = list(csv.DictReader(f))

        found = False
        for i in range(len(rows)):
            if rows[i]['full_name'].strip().lower() == name_to_cancel:
                time3 = rows[i]['time']
                day3 = rows[i]['day']
                del rows[i]
                found = True
                break

        if found:
            if day3 in schedule:
                schedule[day3].append(time3)
                schedule[day3].sort(key=lambda x: datetime.strptime(x, "%H:%M"))

            with open("schedule.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["day", "time"])
                writer.writeheader()
                for d_name, t_list in schedule.items():
                    writer.writerow({"day": d_name, "time": json.dumps(t_list)})

            with open("confirmed.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["full_name", "phone", "day", "time"])
                writer.writeheader()
                writer.writerows(rows)

            print("Booking deleted successfully.")


Vaild_number()
