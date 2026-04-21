from core_logic import handle_intent
from modules.checkin import *

def passenger_menu():
    while True:
        print("\n🧍 Passenger Menu:")
        print("1. Add Passenger")
        print("2. View Passengers")
        print("3. Update Passenger Email")
        print("4. Update Passenger Phone")
        print("5. Update Passenger Name")
        print("6. Delete Passenger")
        print("7. 🔙 Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("Heath: " + handle_intent("add_passenger", ""))

        elif choice == "2":
            print("Heath: " + handle_intent("view_passenger", ""))

        elif choice in ["3", "4", "5", "6"]:
            name = input("Enter passenger name: ").strip()
            pid = get_passenger_id_by_name(name)
            if not pid:
                print("❌ Passenger not found.")
                continue

            if choice == "3":
                email = input("Enter new email: ").strip()
                user_input = f"{pid} {email}"
                print("Heath: " + handle_intent("update_email", user_input))

            elif choice == "4":
                phone = input("Enter new phone: ").strip()
                user_input = f"{pid} {phone}"
                print("Heath: " + handle_intent("update_phone", user_input))

            elif choice == "5":
                new_name = input("Enter new name: ").strip()
                user_input = f"{pid} {new_name}"
                print("Heath: " + handle_intent("update_name", user_input))

            elif choice == "6":
                confirm = input(f"Are you sure you want to delete passenger '{name}'? (y/n): ").strip().lower()
                if confirm == "y":
                    print("Heath: " + handle_intent("delete_passenger", str(pid)))
                else:
                    print("Heath: Deletion cancelled.")

        elif choice == "7":
            break

        else:
            print("❌ Invalid choice.")



def flight_menu():
    while True:
        print("\n✈️ Flight Menu:")
        print("1. Add Flight")
        print("2. View All Flights")
        print("3. View Flights by Destination")
        print("4. View Flights by Departure City")
        print("5. View Flight by Flight Number")
        print("6. Update Flight")
        print("7. Delete Flight")
        print("8. 🔙 Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        intent_map = {
            "1": "add_flight",
            "2": "get_all_flights",
            "3": "get_flight_by_destination",
            "4": "get_flight_by_departure",
            "5": "get_flight_by_number",
            "6": "update_flight",
            "7": "delete_flight"
        }

        if choice == "3":
            city = input("Heath: Which city are you looking flights to? ")
            print("Heath: " + handle_intent("get_flight_by_destination", city))
        elif choice == "4":
            city = input("Heath: From which city are you trying to see the departing flights? ")
            print("Heath: " + handle_intent("get_flight_by_departure", city))
        elif choice == "5":
            flight_number = input("Heath: Please mention the flight number (e.g., AI203 or EK506): ")
            print("Heath: " + handle_intent("get_flight_by_number", flight_number))
        elif choice in intent_map:
            print("Heath: " + handle_intent(intent_map[choice], ""))
        elif choice == "8":
            break
        else:
            print("❌ Invalid choice.")



def checkin_menu():
    while True:
        print("\n🛄 Check-In Menu:")
        print("1. Perform Check-In")
        print("2. View All Check-Ins")
        print("3. Get Check-In Status")
        print("4. Update Check-In Status")
        print("5. 🔙 Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        intent_map = {
            "1": "check_in",
            "2": "view_all_checkins",
            "3": "get_checkin_status",
            "4": "update_checkin_status"
        }

        if choice in intent_map:
            print("Heath: " + handle_intent(intent_map[choice], ""))
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice.")


def security_menu():
    while True:
        print("\n🛂 Security Check Menu:")
        print("1. Perform Security Check")
        print("2. View All Security Status")
        print("3. Get Security Status")
        print("4. Update Security Status")
        print("5. 🔙 Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter passenger name: ").strip()
            flight = input("Enter flight number: ").strip()
            pid = get_passenger_id_by_name(name)
            fid = get_flight_id_by_number(flight)
            if pid and fid:
                user_input = f"{pid} {fid}"
                print("Heath: " + handle_intent("security_check", user_input))
            else:
                print("❌ Invalid passenger or flight.")

        elif choice == "2":
            print("Heath: " + handle_intent("view_all_security_status", ""))

        elif choice == "3":
            name = input("Enter passenger name: ").strip()
            flight = input("Enter flight number: ").strip()
            pid = get_passenger_id_by_name(name)
            fid = get_flight_id_by_number(flight)
            if pid and fid:
                user_input = f"{pid} {fid}"
                print("Heath: " + handle_intent("get_security_status", user_input))
            else:
                print("❌ Invalid passenger or flight.")

        elif choice == "4":
            name = input("Enter passenger name: ").strip()
            flight = input("Enter flight number: ").strip()
            status = input("Is the passenger cleared? (yes/no): ").strip().lower()
            cleared = "1" if status == "yes" else "0"
            pid = get_passenger_id_by_name(name)
            fid = get_flight_id_by_number(flight)
            if pid and fid:
                user_input = f"{pid} {fid} {cleared}"
                print("Heath: " + handle_intent("update_security_status", user_input))
            else:
                print("❌ Invalid passenger or flight.")

        elif choice == "5":
            break

        else:
            print("❌ Invalid choice.")



def menu_loop():
    while True:
        print("\n📋 Heath's Main Menu:")
        print("1. Passenger Management")
        print("2. Flight Management")
        print("3. Check-In System")
        print("4. Security Check")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            passenger_menu()
        elif choice == "2":
            flight_menu()
        elif choice == "3":
            checkin_menu()
        elif choice == "4":
            security_menu()
        elif choice == "5":
            confirm = input("⚠️ Are you sure you want to exit the program? (y/n): ").strip().lower()
            if confirm == "y":
                print("Heath: Goodbye! Have a safe and happy journey ahead.")
                print("Thanks for using Heath ✈️")
                print("~ Built by Soham Bhola ")
                exit()
            else:
                print("🔁 Back to main menu.")

        else:
            print("❌ Invalid choice. Try again.")
