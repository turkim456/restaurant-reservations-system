




   
# Restaurant Reservation System
#### Description:
This project is a Restaurant Reservation System written in Python.
It allows users to create, view, and cancel reservations through a command-line menu.
Booking data is stored in CSV files, while available time slots are managed automatically.
The project also includes a setup file that generates and updates a 7-day schedule 
and removes expired bookings

##  How to Run
To ensure the system has the most up-to-date schedule, follow these steps:

1. **Initialize the data:** Run the setup script first to generate this week's dates.
   ```bash
   python setup_project.py
2. **Start the application:** Run the main program to make a reservation.
   python main_code.py


**main_code file:**

At first, two lists are created: available_times and days_list,
to associate times with specific days.

Then an empty dictionary called schedule is created to store data
from schedule.csv. Inside a try block, the file is opened in read mode.
A variable called reader is created, then a for loop with an iterator
variable called row reads each day and its times from schedule.csv,
which was created in the setup file.

If the file is not found, an error message is printed and the program exits.

---

## FUNCTIONS

---

### 1- menu()

**Function description:**
Displays a welcome message and shows the available services
So the user can choose one.

**How it works:**
Prints a formatted message to the terminal with 4 options.

---

### 2- Vaild_number()

**Function description:**
Reads the user's input and checks if it is in the range (1-4).
If not, the terminal is cleared, and the user is re-prompted
until a valid number is entered.

**How it works:**

A while True loop runs menu() first, then creates an input
variable called user_input with the message "Choose a service (1-4)".

**Case 1 - User enters 1 (New Booking):**
A variable called saved_name stores the result of new_booking().
After the function runs, a message is printed confirming the booking.
Then an input variable called next_step asks what the user wants next:
- 2 → show booking details (runs show_booking(saved_name),
  passing saved_name directly to avoid asking the user
  for their name again, since it was just entered)
- 0 → exit using sys.exit()
- any key → return to main menu

**Case 2 - User enters 2 (Show Booking):**
Runs show_booking() with no argument (saved_name defaults to None),
So the user is asked to type their name manually.
After displaying the details, the user chooses:
- 0 → exit
- any key → return to main menu

**Case 3 - User enters 3 (Cancel Booking):**
Runs cancel_booking() and stores the result.
- result == True  → booking deleted, press Enter to return to menu
- result == False → booking not found, show retry options
- result == None  → user chose No, return to menu silently

**Case 4 - User enters 4 (Exit):**
Prints "Bye Bye" then stops the program using sys.exit().

**Case 5 - User enters an invalid number:**
Runs os.system('cls' if os.name == 'nt' else 'clear')
- cls   → clears the terminal on Windows
- clear → clears the terminal on Mac/Linux

Prints "Please enter a valid number (1-4)" and re-prompts the user.
If the user keeps entering wrong input, Case 5 repeats
until a valid number is entered.

---

### 3- new_booking()

**Function description:**
This function allows a user to make a new booking. It displays all
available days with their times. The user selects a day and time by
number, then fills in their personal information (first name, last name,
phone). If a selected day has no available times, the function returns None.

**How it works:**

**PART 1 - Choose the Date:**
- dates_list: a copy of schedule.keys() converted to a list.
  The .keys() method returns only the days without times.
- show_date(): a nested function that uses a for loop with enumerate()
  to display dates as numbered options. This is user-friendly — the user
  types a number instead of a full date string, which avoids typos that
  the dictionary cannot handle.
- A while True loop runs until the user enters a valid number.
  If the input is out of range, an error message is shown and
  The user is re-prompted.
- chosen_day = dates_list[int(choice) - 1]
  Converts the entered number to the actual day value.

**PART 2 - Choose the Time:**

- Case 1 - Day is fully booked:
  If schedule[chosen_day] is empty, print "All times full for this day!"
  and return None.

- Case 2 - Invalid input:
  If the entered number is not in the valid range,
  Re-prompt the user again and again until valid input is entered.

- Case 3 - Valid time selected:
  chosen_time = schedule[chosen_day][int(chosen_time_num) - 1]
  Converts the entered number to the actual time value.
  Then collect user information:
  - First name → must be alphabetic and at least 3 characters.
  - Last name  → must be alphabetic and at least 3 characters.
  - Phone      → must be digits and exactly 10 characters.
  - full_name  → f"{fname} {lname}"
  Each field uses a while loop that re-prompts until valid input.

**PART 3 - Save to confirmed.csv:**
The booking is saved with fields: full_name, phone, day, and time.
If the file does not exist, a header row is written first.
This step confirms the booking is successful.

**PART 4 - Update schedule.csv:**
- schedule[chosen_day].remove(chosen_time)
  Removes the chosen time from the schedule dictionary so
  other users cannot book the same slot.
- The updated schedule is then rewritten to schedule.csv.
- Finally, a confirmation message is printed:
  "Booking confirmed for {full_name}!" and the full name is returned.

---

### 4- show_booking()

**Function description:**
This function allows users who already have a booking to view their
booking details (full name, phone, day, and time) by searching with
their full name.

**How it works:**

show_booking(saved_name=None) handles two cases:

- Case 1 (user already booked and reopened the program):
  If no parameter is passed, saved_name defaults to None.
  The function asks the user to type their first and last name to search.
  It opens confirmed.csv in read mode and compares the input with each record.
  - If found     → print full name, phone, day, and time.
  - If not found → print "No booking found with this name."

- Case 2 (user just completed a new booking):
  The saved_name is passed directly from new_booking().
  The function immediately compares it with each record in confirmed.csv.
  - If found     → print booking details.
  - If not found → print "No booking found with this name."

---

### 5- cancel_booking()

**Function description:**
This function allows a user to cancel an existing booking by entering
their full name and phone number. The booking details are displayed
for confirmation (1-Yes / 2-No) before deletion.

**How it works:**

1. Check if confirmed.csv exists to avoid opening an empty file.
2. Validate name and phone using while loops — re-prompt until correct input.
3. Open confirmed.csv in read mode and convert each row to a list called
   rows, since lists support deletion, unlike dictionaries.
4. Create found=False, then loop through rows to find a match.
   - If found     → display: full name, phone, day, and time.
   - If not found → print "No booking found with that name and phone."
5. Ask the user to press any key to read the information.
   Create options2 = ["Yes", "No"] for confirmation.
6. Use a while loop to show "Please confirm canceling" and enumerate
   options2 using a for loop with variables j and option.
7. Create a confirmation input asking to choose (1-2):
   - If 1 → store time and day in time3, day3, delete row, set found=True.
   - If 2 → print "Deletion canceled." and return None.
8. If found:
   - Check if day3 is in the schedule.
   - schedule[day3].append(time3) → restore the time slot.
   - schedule[day3].sort(...) → keep times in order.
9. Rewrite both files:
   - schedule.csv  → updated so others can book the canceled slot.
   - confirmed.csv → user's booking is removed using writerows(rows).
10. Print "Booking deleted successfully." and return True.

---

## SETUP FILE

**setup.py file:**

This file is responsible for initializing and updating the 7-day booking
schedule daily. It also removes expired bookings from confirmed.csv
to keep the system clean and up to date.

---

**How it works:**

**PART 1 - Define Available Times and Days:**
- available_times: a list of all time slots from 7:00 to 12:30.
- days: a list of the 7 days of the week.

**PART 2 - Check if Already Updated Today:**
- today_str: stores today's date as a string in format "YYYY-MM-DD"
  using datetime.now().strftime().
- date_file: the name of the file "last_update.txt" that tracks
  the last time the schedule was updated.
- already_updated = False by default.
- If last_update.txt exists and contains today's date,
  already_updated is set to True and the update is skipped.
  This ensures the schedule is only regenerated once per day.

**PART 3 - Generate the 7-Day Schedule (if not already updated):**
- An empty dictionary called schedule is created.
- A for loop runs 7 times (i = 0 to 6):
  - target_date = today + timedelta(days=i) → calculates each day.
  - date_key is formatted as "YYYY-MM-DD (DayName)" using strftime().
  - Each day is assigned a full copy of available_times.
- The schedule dictionary is written to schedule.csv with
  fields: day, time. Times are stored as JSON strings.
- today_str is written to last_update.txt to mark the update as done.

**PART 4 - Clean Up confirmed.csv:**
- If confirmed.csv exists, it is opened in read mode.
- A for loop goes through each row and checks the booking date:
  - booking_date = row['day'][:10] → extracts "YYYY-MM-DD" from the day field.
  - If booking_date >= today → keep the row (future or today's booking).
  - If booking_date < today  → discard the row (expired booking).
- The filtered rows are rewritten back to confirmed.csv,
  removing all past bookings automatically.
- A message is printed: "Cleanup finished: Old history removed."



### schedule.csv


The `schedule.csv` file stores all available booking dates and their corresponding time slots.

**Structure:**
- `day`: stores the booking date in the format `YYYY-MM-DD (DayName)`.
- `time`: stores a JSON array containing all available times for that d



#### How it is used

The file is generated and updated by `setup.py`. When a booking is made, the selected time
is removed from the corresponding day. When a booking is canceled, the time slot is restored and written back to the fil


### confirmed.csv

The `confirmed.csv` file stores all confirmed bookings created by users.

#### Structure

- `full_name`: stores the user's first and last name.
- `phone`: stores the user's phone number.
- `day`: stores the selected booking date.
- `time`: stores the selected booking time.

#### How it is used

- When a user creates a new booking, their information is saved to this file.
- The `show_booking()` function searches this file to display booking details.
- The `cancel_booking()` function searches this file using the user's name and phone number.
- When a booking is canceled, the corresponding record is removed from the file.
- The file acts as the main storage for all active bookings in the system.


### last_update.txt

The `last_update.txt` file stores the date of the most recent schedule update.

#### Structure

- A single date in the format `YYYY-MM-DD`.

#### How it is used

- The file is checked whenever `setup.py` runs.
- If the stored date matches today's date, the schedule update is skipped.
- If the stored date is different from today's date, a new 7-day schedule is generated and the file is updated.
- This prevents the schedule from being regenerated multiple times on the same day.
