import pymysql.cursors
from db_config import get_connection
from datetime import datetime 
import pymysql
from tabulate import tabulate

def add_security_check_record(passenger_id, flight_id, cleared=0):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO security_check (passenger_id, flight_id, cleared)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (passenger_id, flight_id, cleared))
        connection.commit()
    except Exception as e:
        print(f"Error adding security check record: {e}")
    finally:
        connection.close()

def update_security_status(passenger_id, flight_id, cleared):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE security_check
                SET cleared = %s, timestamp = CURRENT_TIMESTAMP
                WHERE passenger_id = %s AND flight_id = %s
            """
            cursor.execute(query, (cleared, passenger_id, flight_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating security status: {e}")
    finally:
        connection.close()

def get_security_status(passenger_id, flight_id):
    try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT s.passenger_id, p.name, s.flight_id, s.cleared, s.timestamp
                FROM security_check s
                JOIN passengers p ON s.passenger_id = p.passenger_id
                WHERE s.passenger_id = %s AND s.flight_id = %s
            """
            cursor.execute(query, (passenger_id, flight_id))
            result = cursor.fetchone()
            connection.close()

            if result:
                return (
                    result["passenger_id"],
                    result["name"],
                    result["flight_id"],
                    result["cleared"],
                    result["timestamp"]
            )
            else:
                return None

    except Exception as e:
        print(f"DB error in get_security_status: {e}")
        return None
    
def view_all_security_status():
    try:
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT security_check.passenger_id, passengers.name, security_check.flight_id, security_check.cleared, security_check.timestamp
            FROM security_check
            JOIN passengers ON security_check.passenger_id = passengers.passenger_id
        """
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        if not records:
            return "No security check records found."
        table = []
        for row in records:
            table.append([
                row["passenger_id"],
                row["name"],
                row["flight_id"],
                "Cleared" if row["cleared"] else "Pending",
                row["timestamp"]
            ])
        
        headers = ["Passenger ID", "Name", "Flight ID", "Status", "Last Updated"]
        return "\n" + tabulate(table, headers = headers, tablefmt="fancy_grid")
    except Exception as e:
        return f"Error fetching all security statuses: {e}" 

def security_check_interaction(passenger_id, flight_id=None):
    try:
        if not flight_id:
            flight_id = int(input("Enter flight ID: ").strip())

        status = get_security_status(passenger_id, flight_id)
        if status:
            print(f"Current Security Status: {'Cleared' if status[0] else 'Pending' } (Last Updated: {status[1]})")
            confirm = input("Do you want to update the status? (yes/no): ").strip().lower()
            if confirm != 'yes':
                return "Update cancelled."
        else:
            print("No security record found. Creating a new one.")
        
        cleared_input = input("Has the passenger cleared security? (yes/no): ").strip().lower()
        cleared = 1 if cleared_input == 'yes' else 0
        if status:
            update_security_status(passenger_id, flight_id, cleared)
            return f"Security status updated: {'Cleared' if cleared else 'Pending'}"
        else:
            add_security_check_record(passenger_id, flight_id, cleared)
            return f"Security status created: {'Cleared' if cleared else 'Pending'}"
    except Exception as e:
        return f"Error in security check interaction: {e}"