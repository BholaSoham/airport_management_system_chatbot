import pymysql
import csv
from tabulate import tabulate
from db_config import get_connection
from datetime import datetime

def add_flight(flight_number, airline, departure_city, arrival_city, departure_time, arrival_time, status, gate):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO flights (flight_number, airline, departure_city, arrival_city, departure_time, arrival_time, status, gate)
            VALUES (%s, %s, %s,%s, %s, %s, %s, %s)
            """
            values = (flight_number, airline, departure_city, arrival_city, departure_time, arrival_time, status, gate)
            cursor.execute(sql, values)
        connection.commit()
        print("✅ Flight added successfully.")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        connection.close()

def is_valid_datetime(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def get_all_flights():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM flights")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching all flights: {e}")
        return []

def get_flight_by_number(flight_number):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM flights WHERE flight_number = %s"
            cursor.execute(sql,(flight_number,))
            return cursor.fetchone()
    except Exception as e:
        print("❌ Error:", e)
    finally:
        connection.close()

def get_flight_by_departure(departure_city):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM flights WHERE departure_city = %s"
            cursor.execute(query, (departure_city,))
            result = cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        print(f"Error fetching flights from {departure_city}: {e}")
        return []

def get_flight_by_destination(destination_city):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM flights WHERE arrival_city = %s"
            cursor.execute(sql,( destination_city ,))
            return cursor.fetchall()
    except Exception as e:
        print("❌ Error fetching the flights by destination:", e)
    finally:
        connection.close()

def update_flight_field(flight_number, field, new_value):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = f"UPDATE flights SET {field} = %s WHERE flight_number = %s"
            cursor.execute(query, (new_value, flight_number))
            connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error updating flight in DataBase: {e}")

def update_flight_interaction():
    try:
        flight_number = input("Enter flight number to update: ").strip().upper()
        flight = get_flight_by_number(flight_number)
        if not flight:
            return f"No flight found with number {flight_number}"
        print("\nCurrent flight details:")
        print("\n" + tabulate([[flight["flight_id"], flight["flight_number"], flight["airline"],
                         flight["departure_city"], flight["arrival_city"], flight["departure_time"],
                         flight["arrival_time"], flight["status"], flight["gate"]]],
                       headers=["ID", "Flight Number", "Airline", "From", "To", "Depart Time", "Arrival Time", "Status", "Gate"],
                       tablefmt="grid" ))
        field_map = {
            "airline": "airline",
            "departure city": "departure_city",
            "arrival city": "arrival_city",
            "departure time": "departure_time",
            "arrival time": "arrival_time",
            "status": "status",
            "gate": "gate"
        }
        field_input = input(f"Which field would you like to update? {list(field_map.keys())}: ").strip().lower()
        if field_input not in field_map:
            return f"'{field_input}' is not allowed to be updated."

        field = field_map[field_input]
        new_value = input(f"Enter new value for '{field_input}': ").strip()
        confirm = input(f"Confirm update '{field_input}' from '{flight[field]}' to '{new_value}'? (yes/no): ").lower()
        if confirm != "yes":
            return "Update cancelled."

        update_flight_field(flight_number, field, new_value)
        return f"Flight {flight_number} updated successfully: {field_input} → {new_value}"

    except Exception as e:
        return f"Error updating flight: {e}"

def delete_flight_by_number(flight_number):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM flights WHERE flight_number = %s"
            cursor.execute(query, (flight_number,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
    except Exception as e:
        print(f"Error deleting flight: {e}")
        return False

def delete_flight_interaction():
    try:
        flight_number = input("Enter flight number to delete: ").strip().upper()
        flight = get_flight_by_number(flight_number)

        if not flight:
            return f"No flight found with number {flight_number}"
        print("\nFlight Found:")
        print("\n" + tabulate([[flight["flight_id"], flight["flight_number"], flight["airline"],
                         flight["departure_city"], flight["arrival_city"], flight["departure_time"],
                         flight["arrival_time"], flight["status"], flight["gate"]]],
                       headers=["ID", "Flight Number", "Airline", "From", "To", "Depart Time", "Arrival Time", "Status", "Gate"],
                       tablefmt="grid" ))
        confirm = input(f"Are you sure you want to delete flight '{flight_number}' (yes/no): ")
        if confirm != "yes":
            return "Delete operation terminated"
        success = delete_flight_by_number(flight_number)
        if success:
            return f"flight {flight_number} deleted successfully."
        else:
            return "Failed to delete flight from the datavase."
    except Exception as e:
        return f"Error deleting flight : {e}"

def load_city_names(file_path):
    city_names = set()
    with open(file_path, mode = 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = row['city'].strip().lower()
            if city:
                city_names.add(city)
    return city_names

def extract_city_from_input(user_input, city_names):
    user_input_lower = user_input.lower()
    sorted_cities = sorted(city_names, key = lambda x: -len(x))
    for city in sorted_cities:
        if city in user_input_lower:
            return city.title()
    return None

