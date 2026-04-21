from tabulate import tabulate
from nlp_brain import extract_passenger_info, extract_flight_number
from modules.crud_passengers import (
    add_passenger, delete_passenger,
    update_passenger_email, update_passenger_name,
    update_passenger_phone, get_passenger_by_name,
    get_multiple_passengers, get_all_passengers,
    get_passenger_by_id
)
from modules.crud_flights import (
    get_flight_by_destination, get_flight_by_number, 
    extract_city_from_input, load_city_names,
    add_flight, get_all_flights, get_flight_by_departure,
    update_flight_interaction, delete_flight_interaction
)
from modules.security_checks import (
    security_check_interaction, get_security_status,
    add_security_check_record, update_security_status,
    view_all_security_status
)
from modules.checkin import (
    add_checkin, get_checkin_status,
    view_all_checkins, get_passenger_id_by_name,
    update_checkin_status, get_flight_id_by_number
)

def handle_intent(intent, user_input):
    # FLIGHTS
    if intent == "get_flight_by_destination":
        try:
            city_names = load_city_names("airports.csv")
            destination = extract_city_from_input(user_input, city_names)
            if not destination:
                return "Which city are you looking flights to?"
            flights = get_flight_by_destination(destination)
            if flights:
                table_data = [
                    [
                    f["flight_id"],
                    f["flight_number"],
                    f["airline"],
                    f["departure_city"],
                    f["arrival_city"],
                    f["departure_time"],
                    f["arrival_time"],
                    f["status"],
                    f["gate"]
                    ]
                    for f in flights
                ]

                headers = ["ID", "Flight Number", "Airline", "From", "To", "Depart Time", "Arrival Time", "Status", "Gate"]

                return "\n" + tabulate(table_data, headers=headers, tablefmt="grid")

            else:
                return f"No flights found to {destination}"
        except Exception as e:
            return f"Error fetching flights:{e}"

    elif intent == "get_flight_by_number":
        try:
            flight_number = extract_flight_number(user_input)
            if not flight_number:
                return "Please mention the flight number in the format like AI203 or EK506."
            flight = get_flight_by_number(flight_number)
            if flight:
                flight_data = [
                flight["flight_id"],
                flight["flight_number"],
                flight["airline"],
                flight["departure_city"],
                flight["arrival_city"],
                flight["departure_time"],
                flight["arrival_time"],
                flight["status"],
                flight["gate"]
            ]
                return "\n" + tabulate(
                [flight_data],
                headers = ["ID","Flight Number","Airline","From","To","Depart Time","Arrival Time","Status","Gate"],
                tablefmt = "grid"
                )
            else:
                return f"No flight found with number {flight_number}"
        except Exception as e:
            return f"Error fetching flight details of {flight_number}: {e}"

    elif intent == "get_flight_by_departure":
         try:
            city_names = load_city_names("airports.csv")
            departure = extract_city_from_input(user_input ,city_names)
            if not departure:
                return "From which city are you trying to see the departing flights?"
            flights = get_flight_by_departure(departure)
            if flights:
                formatted = [
                    [
                        flight["flight_id"],
                        flight["flight_number"],
                        flight["airline"],
                        flight["departure_city"],
                        flight["arrival_city"],
                        flight["departure_time"],
                        flight["arrival_time"],
                        flight["status"],
                        flight["gate"]
                    ]
                    for flight in flights 
            ]
                return "\n" + tabulate(
                    formatted,
                    headers = ["ID","Flight Number","Airline","From","To","Depart Time","Arrival Time","Status","Gate"],
                    tablefmt="grid"
                )
            else:
                return f"No flights found departing from {departure}"
         except Exception as e:
             return f"Error fetching departing flights: {e}"
             
    elif intent == "get_all_flights":
        try:
            flights = get_all_flights()
            if flights:
                formatted_flights = [
                    [
                        flight["flight_id"],
                        flight["flight_number"],
                        flight["airline"],
                        flight["departure_city"],
                        flight["arrival_city"],
                        flight["departure_time"],
                        flight["arrival_time"],
                        flight["status"],
                        flight["gate"]
                    ]
                    for flight in flights 
            ]
                return "\n" + tabulate(
                    formatted_flights,
                    headers = ["ID", "Flight Number", "Airline", "From", "To", "Depart Time", "Arrival Time", "Status", "Gate"],
                    tablefmt="grid"
                )
            else:
                return "No flights found in the system."
        except Exception as e:
            return f"Error fetching all flights: {e}"

    elif intent == "add_flight":
        try:
            flight_number = input("Enter flight number: ").strip().upper()
            airline = input("Enter airline:").strip()
            source = input("Enter source city: ").strip().title()
            destination = input("Enter destination city: ").strip().title()
            departure_time = input("Enter departure time (YYYY-MM-DD HH:MM:SS):")
            arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM:SS):")
            status = input("Enter flight status (On Time / Delayed / Cancelled):").strip()
            gate = input("Enter gate number: ").strip()
            add_flight(flight_number, airline, source, destination, departure_time, arrival_time, status, gate)

            return f"Flight {flight_number} added successfully"
        except Exception as e:
            return str(e)

    elif intent == "update_flight":
        return update_flight_interaction()
    
    elif intent == "delete_flight":
        return delete_flight_interaction()

    # CHECKIN
    elif intent == "check_in":
        try:
            name = input("Enter passenger name: ").strip()
            fid = input("Enter flight number: ").strip()
            pid = get_passenger_id_by_name(name)
            if not pid:
                return "❌ Passenger not found."
            result = add_checkin(pid, fid)
            return result
        except Exception as e:
            return f"Error during check-in: {e}"
    
    elif intent == "update_checkin_status":
        name = input("Enter passenger name: ").strip()
        flight = input("Enter flight number: ").strip()
        pid = get_passenger_id_by_name(name)
        if pid and flight:
            status = input("Mark as checked-in? (yes/no): ").strip().lower()
            is_checked = True if status == "yes" else False
            return update_checkin_status(pid, flight, is_checked)
        else:
            return "❌ Invalid passenger or flight."

    
    elif intent == "get_checkin_status":
        try:
            name = input("Enter passenger name: ").strip()
            fid = input("Enter flight number:").strip()
            pid = get_passenger_id_by_name(name)
            if pid:
                return get_checkin_status(pid, fid)
            else:
                return "❌ No passenger found with that name."
        except Exception as e:
            return f"Error fetching check-in status: {e}"
    
    elif intent == "view_all_checkins":
        return view_all_checkins()

    # SECURITY CHECK
    elif intent == "security_check":
        try:
            if user_input:
                parts = user_input.strip().split()
                pid = int(parts[0])
                fid = int(parts[1])
                result = security_check_interaction(pid, fid)
            else:
                pid = int(input("Enter passenger ID: ").strip())
                result = security_check_interaction(pid)
            return result
        except Exception as e:
            return f"Error during security check: {e}"
    
    elif intent == "get_security_status":
        try:
            if user_input:
                parts = user_input.strip().split()
                pid = int(parts[0])
                fid = parts[1]
            else:
                pid = int(input("Enter passenger ID: ").strip())
                fid = input("Enter flight ID: ").strip()
            status = get_security_status(int(pid), fid)            
            if status is None:
                return "No security status found for this passenger and flight."
            else:
                table = [[
                    status[0],
                    status[1],
                    status[2],
                    "Cleared" if status[3] else "Pending",
                    status[4].strftime("%Y-%m-%d %H:%M:%S")
                ]]
                headers = ["Passenger ID", "Name", "Flight ID", "Status", "Last Updated"]
                return "\n" + tabulate(table, headers=headers, tablefmt= "fancy_grid")
            
        except Exception as e:
            return f"Error retrieving security status: {e}"
    
    elif intent == "view_all_security_status":
        return view_all_security_status()
    
    elif intent == "update_security_status":
        try:
            if user_input:
                parts = user_input.strip().split()
                pid = int(parts[0])
                fid = parts[1]
                cleared = int(parts[2])
            else:
                pid = input("Enter passenger ID: ").strip()
                fid = input("Enter flight ID: ").strip()
                cleared_input = input("Has the passenger cleared security? (yes/no): ").strip().lower()
                if cleared_input not in ['yes','no']:
                    return "invaild input. Please enter 'yes' or 'no'."
                cleared = 1 if cleared_input == 'yes' else 0
            update_security_status(int(pid), fid, cleared)
            return f"Security status updated to {'Cleared' if cleared else 'Pending'} for Passenger ID {pid} on Flight {fid}."
        except Exception as e:
                return f"Error updating security status: {e}"      
    
    # BAGGAGE
    elif intent == "baggage_info":
        return "You can carry 15kg check-in baggage and 7kg cabin baggage"
    
    elif intent == "greeting":
        return "Hello! How can I assist you today at the airport?"
    
    elif intent == "goodbye":
        return "Thank you for visting. Have a safe journey!"
    
    elif intent == "exit":
        return "Goodbye! Have a safe and happy journey ahead."
    
    # PASSENGER OPERATIONS
    elif intent == "add_passenger":
        try:
            name = input("Enter name: ")
            passport = input("Enter passport number: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            age = input("Enter age: ")
            add_passenger(name, passport, email, phone, age)
            new_passenger = get_passenger_by_name(name)
            if new_passenger:
                return "✅ Passenger added successfully:\n" + tabulate(
                    [new_passenger],
                    headers="keys" if isinstance(new_passenger, dict) else ["ID", "Name", "Passport", "Email", "Phone", "Age"],
                    tablefmt="grid"
                )
            else:
                return "Passenger added but couldn't fetch details."
        except Exception as e:
            return f"Error while adding the passenger: {e}"

    elif intent == "delete_passenger":
        try:
            if user_input:
                passenger_id = int(user_input.strip())
            else:
                passenger_id = int(input("Enter the passenger ID to delete: "))            
            
            delete_passenger(passenger_id)
            return "✅ Passenger has been deleted successfully."
        except Exception as e:
            return f"Error while deleting the passenger: {e}"

    elif intent == "view_passenger":
        names, number = extract_passenger_info(user_input)
        if names:
            results = []
            for name in names:
                passenger = get_passenger_by_name(name)
                if passenger:
                    results.append(passenger)
            if results:
                return "\n" + tabulate(results, headers="keys" if isinstance(results[0], dict) else ["ID", "Name", "Passport", "Email", "Phone", "Age"], tablefmt="grid")
            else:
                return f"No passenger(s) found for names: {', '.join(names)}"
        elif number:
            passengers = get_multiple_passengers(number)
            if passengers:
                return "\n" + tabulate(passengers, headers="keys" if isinstance(passengers[0], dict) else ["ID", "Name", "Passport", "Email", "Phone", "Age"], tablefmt="grid")
            else:
                return "No passenger data found."
        else:
            passengers = get_all_passengers()
            if passengers:
                return "\n" + tabulate(passengers, headers="keys" if isinstance(passengers[0], dict) else ["ID", "Name", "Passport", "Email", "Phone", "Age"], tablefmt="grid")
            else:
                return "No passengers in the database."

        
    elif intent == "update_email":
        try:
            if user_input:
                parts = user_input.strip().split()
                pid = int(parts[0])
                new_email = parts[1]
            else:
                pid = input("Enter passenger ID: ")
                new_email = input("Enter new email: ")
                
            update_passenger_email(pid, new_email)
            updated = get_passenger_by_id(pid)
            return "✅ Email updated successfully:\n" + tabulate(
                [updated],
                headers="keys" if isinstance(updated, dict) else ["ID", "Name", "Passport", "Email", "Phone", "Age"],
                tablefmt="grid"
            )
        except Exception as e:
            return f"Error while updating the passenger's email address: {e}"

    elif intent == "update_phone":
        try:
            if user_input:
                parts = user_input.strip().split()
                pid = int(parts[0])
                new_phone = parts[1]
            else:
                pid = int(input("Enter passenger ID: "))
                new_phone = input("Enter new phone number: ")

            update_passenger_phone(pid, new_phone)
            updated = get_passenger_by_id(pid)
            return "✅ Phone number updated successfully:\n" + tabulate(
                [updated],
                headers="keys" if isinstance(updated, dict) else ["ID", "Name", "Passport", "Email", "Phone", "Age"],
                tablefmt="grid"
            )
        except Exception as e:
            return f"Error while updating the passengers's phone number: {e}"

    elif intent == "update_name":
        try:
            if user_input:
                parts = user_input.strip().split()
                pid = int(parts[0])
                new_name = " ".join(parts[1:])
            else:
                pid = int(input("Enter passenger ID: "))
                new_name = input("Enter new name: ")

            update_passenger_name(pid,new_name)
            updated = get_passenger_by_id(pid)
            return "✅ Name updated successfully:\n" + tabulate(
                [updated],
                headers="keys" if isinstance(updated, dict) else ["ID", "Name", "Passport", "Email", "Phone", "Age"],
                tablefmt="grid"
            )
        except Exception as e:
            return f"Error while updating the name of the passenger: {e}"

    else:
        return "Sorry, I didn't understand that. Could you please rephrase?"
    