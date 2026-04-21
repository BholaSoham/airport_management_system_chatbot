import pymysql
from db_config import get_connection  

def insert_mock_passengers():
    connection = get_connection() 
    try:
        with connection.cursor() as cursor:
            passengers = [
                ("Sarah Johnson", "P1234567", "sarah@example.com", "1234567890", 28),
                ("Mike Brown", "P7654321", "mike@example.com", "9876543210", 35),
                ("Alex Carter", "P1122334", "alex@example.com", "9988776655", 42)
            ]

            insert_query = """
                INSERT INTO passengers (name, passport_number, email, phone, age)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.executemany(insert_query, passengers)
            connection.commit()
            print("✅ Mock passengers inserted successfully!")

    finally:
        connection.close()

if __name__ == "__main__":
    insert_mock_passengers()
