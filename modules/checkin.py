import pymysql
from tabulate import tabulate
from db_config import get_connection

def add_checkin(passenger_id, flight_number):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # Check if check-in already exists
            cursor.execute("""
                SELECT * FROM checkin 
                WHERE passenger_id = %s AND flight_number = %s
            """, (passenger_id, flight_number))
            if cursor.fetchone():
                return "⚠️ Check-in record already exists."

            # Insert new check-in record
            cursor.execute("""
                INSERT INTO checkin (passenger_id, flight_number, checked_in, last_updated)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            """, (passenger_id, flight_number, False))
            connection.commit()
            return "✅ Check-in record added successfully."
    except Exception as e:
        return f"❌ Error adding check-in: {e}"
    finally:
        connection.close()

def get_checkin_status(passenger_id, flight_number):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT p.name, c.passenger_id, c.flight_number, c.checked_in, c.last_updated
                FROM checkin c
                JOIN passengers p ON c.passenger_id = p.passenger_id
                WHERE c.passenger_id = %s AND c.flight_number = %s
            """
            cursor.execute(query, (passenger_id, flight_number))
            result = cursor.fetchone()
            if result:
                headers = ["Name", "Passenger ID", "Flight ID", "Checked-In", "Last Updated"]
                return "\n" + tabulate([result], headers="keys", tablefmt="fancy_grid")
            else:
                return "❌ No check-in record found for this passenger and flight."
    except Exception as e:
        return f"❌ Error retrieving check-in status: {e}"
    finally:
        connection.close()

def view_all_checkins():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT p.name, c.passenger_id, c.flight_number, c.checked_in, c.last_updated
                FROM checkin c
                JOIN passengers p ON c.passenger_id = p.passenger_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                headers = ["Name", "Passenger ID", "Flight ID", "Checked-In", "Last Updated"]
                return "\n" + tabulate(rows, headers="keys", tablefmt="fancy_grid")
            else:
                return "No check-in record found."
    except Exception as e:
        return f"Error fetching check-in records: {e}"
    finally:
        connection.close()
    
def update_checkin_status(passenger_id, flight_number, checked_in=True):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT checked_in FROM checkin
                WHERE passenger_id = %s AND flight_number = %s
            """, (passenger_id, flight_number))
            row = cursor.fetchone()

            if not row:
                return f"⚠️ No check-in record found for Passenger ID {passenger_id} and Flight '{flight_number}'."
            
            current_status = row["checked_in"]

            if current_status == 1 and checked_in:
                return "🟢 Already checked-in. No update performed."

            cursor.execute("""
                UPDATE checkin
                SET checked_in = %s, last_updated = NOW()
                WHERE passenger_id = %s AND flight_number = %s
            """, (checked_in, passenger_id, flight_number))
            connection.commit()
            if cursor.rowcount == 0:
                return "⚠️ Update attempted but no rows were modified"
            return "✅ Check-in status updated successfully."
    except Exception as e:
        return f"❌ Error updating check-in status: {str(e)}"
    finally:
        connection.close()

def get_passenger_id_by_name(name):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT passenger_id FROM passengers WHERE LOWER(name) = %s", (name,))
            result = cursor.fetchone()
            return result ['passenger_id'] if result else None
    except Exception as e:
        print (f"Error fetching passenger ID: {e}")
        return None
    finally:
        connection.close()

def get_flight_id_by_number(flight_number):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT flight_id FROM flights WHERE LOWER(flight_number) = %s",
                (flight_number.lower().strip(),)
            )
            result = cursor.fetchone()
            return result ['flight_id'] if result else None
    except Exception as e:
        print(f"Error fetching flight ID: {e}")
        return None
    finally:
        connection.close()