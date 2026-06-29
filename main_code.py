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
    print("Error: schedule.csv not found. Please run the setup file first.")
    sys.exit()


def menu():
    print("\nWelcome to our Restaurant")
    print("─" * 40)
    print("What service do you want? Choice number:")
    print("1- New Book")
    print("2- Show Book")
    print("3- Cancel Book")
    print("4- Exit")


def Vaild_number():
    while True:
        menu()
        user_input = input("Choose a service (1-4): ").strip()

        if user_input == "1":
            saved_name = new_booking()
            if saved_name:
                print(f"\nBooking for {saved_name} is done!")
                next_step = input("Press 2 to SHOW details, 0 to EXIT, or any key for MAIN MENU: ").strip()
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
            result = cancel_booking()
            if result == True:
                input("\nCanceled. Press Enter to return to Main Menu...")
            elif result == False:
                while True:
                    print("\nDo you want to try again?")
                    options = ["Yes", "Change services", "Exit"]
                    for i, option in enumerate(options, start=1):
                        print(f"{i}- {option}")

                    retry = input("Choose (1-3): ").strip()

                    if retry == "1":
                        result = cancel_booking()
                        if result == True:
                            input("\nCanceled. Press Enter to return to Main Menu...")
                        break
                    elif retry == "2":
                        break
                    elif retry == "3":
                        sys.exit()
                    else:
                        print("Invalid choice please re-enter again.")
                        input("press any key to continue...")
                        os.system("cls" if os.name == "nt" else "clear")

        elif user_input == "4":
            print("Bye Bye")
            sys.exit()

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n Please enter a valid number (1-4)")


def new_booking():
    global schedule

    dates_list = list(schedule.keys())

    # PART 1: CHOOSE THE DATE
    while True:
        for i, date_label in enumerate(dates_list, start=1):
            print(f"{i} - {date_label}")
        choice = input("Select date number: ")

        if choice.isdigit() and 1 <= int(choice) <= len(dates_list):
            chosen_day = dates_list[int(choice) - 1]
            break
        else:
            print("Out of range, please re-enter.")
            input("press any key to continue...")
            os.system("cls" if os.name == "nt" else "clear")

    # PART 2: CHOOSE THE TIME
    while True:
        if not schedule[chosen_day]:
            print("All times full for this day!")
            return None

        print(f"\nthe times available for {chosen_day}")
        for i, time_label in enumerate(schedule[chosen_day], start=1):
            print(f"{i} - {time_label}", end=" ")
            if i % 6 == 0 and i < len(schedule[chosen_day]):
                print()
                print("─" * 60)
        print("\n")

        chosen_time_num = input("Choose time from above: ")

        if chosen_time_num.isdigit() and 1 <= int(chosen_time_num) <= len(schedule[chosen_day]):
            chosen_time = schedule[chosen_day][int(chosen_time_num) - 1]

            # Validate First Name
            while True:
                fname = input("Enter your First Name: ").strip().capitalize()
                if fname.isalpha() and len(fname) >= 3:
                    break
                print("Invalid name. Please use at least 3 letters.")

            # Validate Last Name
            while True:
                lname = input("Enter your Last Name: ").strip().capitalize()
                if lname.isalpha() and len(lname) >= 3:
                    break
                print("Invalid name. Please use letters only.")

            # Validate Phone Number
            while True:
                phone = input("Enter your 10-digit Phone Number: ").strip()
                if phone.isdigit() and len(phone) == 10:
                    break
                print("Invalid phone. Must be exactly 10 digits.")

            full_name = f"{fname} {lname}"
            break

        else:
            print("Please enter a valid time from the list.")

    # PART 3: SAVE BOOKING TO FILE
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
            "time": chosen_time,
        })

    # PART 4: UPDATE AND SAVE SCHEDULE
    schedule[chosen_day].remove(chosen_time)
    with open("schedule.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["day", "time"])
        writer.writeheader()
        for d_key, t_list in schedule.items():
            writer.writerow({"day": d_key, "time": json.dumps(t_list)})

    print(f"\nBooking confirmed for {full_name}!")
    return full_name


def show_booking(saved_name=None):
    found = False

    if saved_name is None:
        saved_name = input("Enter your First and Last Name: ").strip()
        phone = input("Enter your phone number: ").strip()

        if os.path.exists("confirmed.csv"):
            with open("confirmed.csv", "r") as f:
                reader = csv.DictReader(f)
                for line in reader:
                    if line['full_name'].lower() == saved_name.lower() and line['phone'] == phone:
                        print("\nBooking found:")
                        print(f"Name : {line['full_name']}")
                        print(f"Phone: {line['phone']}")
                        print(f"Day  : {line['day']}")
                        print(f"Time : {line['time']}")
                        print("─" * 40)
                        found = True
    else:
        if os.path.exists("confirmed.csv"):
            with open("confirmed.csv", "r") as f:
                reader = csv.DictReader(f)
                for line in reader:
                    if line['full_name'].lower() == saved_name.lower():
                        print("\nBooking found:")
                        print(f"Name : {line['full_name']}")
                        print(f"Phone: {line['phone']}")
                        print(f"Day  : {line['day']}")
                        print(f"Time : {line['time']}")
                        print("─" * 40)
                        found = True

    if not found:
        print("No booking found.")


def cancel_booking():
    global schedule
    if not os.path.exists("confirmed.csv"):
        print("No bookings found.")
        return False

    # Validate Name
    while True:
        name_to_cancel = input("Enter your name to delete your booking:\n ").strip().lower()
        if name_to_cancel.replace(" ", "").isalpha() and len(name_to_cancel) >= 3:
            break
        print("Invalid name. Please use letters only.")
        input("press any key to continue...")

    # Validate Phone
    while True:
        phone_to_cancel = input("Enter your phone number: ").strip()
        if phone_to_cancel.isdigit() and len(phone_to_cancel) == 10:
            break
        print("Invalid phone. Must be exactly 10 digits.")
        input("press any key to continue...")

    with open("confirmed.csv", "r") as f:
        rows = list(csv.DictReader(f))

    found = False
    for i in range(len(rows)):
        if rows[i]['full_name'].strip().lower() == name_to_cancel and rows[i]['phone'] == phone_to_cancel:

            row_index = i

            print("\nBooking found:")
            print(f"Name : {rows[row_index]['full_name']}")
            print(f"Phone: {rows[row_index]['phone']}")
            print(f"Day  : {rows[row_index]['day']}")
            print(f"Time : {rows[row_index]['time']}")
            input("Press any key to continue...")

            options2 = ["Yes", "No"]
            while True:
                print("Please confirm canceling")
                for j, option in enumerate(options2, start=1):
                    print(f"{j} - {option}")

                confirm = input("Choose (1-2): ").strip()
                if confirm == "1":
                    time3 = rows[row_index]['time']
                    day3 = rows[row_index]['day']
                    del rows[row_index]
                    found = True
                    break
                elif confirm == "2":
                    print("Deletion canceled.")
                    return None
                else:
                    print("Invalid choice.")
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
        return True
    else:
        print("No booking found with that name and phone.")
        input("Press any key to continue...")
        return False


Vaild_number()
