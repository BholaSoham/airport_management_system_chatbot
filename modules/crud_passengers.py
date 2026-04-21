import pymysql
from tabulate import tabulate
from db_config import get_connection


def add_passenger(name, passport_number, email, phone, age):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO passengers (name, passport_number, email, phone, age) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql,(name, passport_number, email, phone, age))
            connection.commit()
    except Exception as e:
        print("❌ Error:", e) 
    finally:
        connection.close()

# Example call
# add_passenger("John Doe", "A1234567", "john@gmail.com", "1234567890","22")

def view_passengers():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM passengers"
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                headers = ["Passenger_ID","Name","Passport Number","Email","Phone","Age"]
                print(tabulate(results, headers=headers, tablefmt="pretty"))
            else:
                print("No passengers found")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        connection.close()

# Example call
# view_passengers()

def update_passenger_email(passenger_id, new_email):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE passengers SET email = %s WHERE passenger_id = %s"
            cursor.execute(sql, (new_email, passenger_id))
        connection.commit()
    except Exception as e:
        print("❌ Error", e)
    finally:
        connection.close()

# Example call
# update_passenger_email(1, "gayjohn@gmail.com")
# view_passengers()

def update_passenger_name(passenger_id, new_name):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE passengers SET name = %s WHERE passenger_id = %s"
            cursor.execute(sql, (new_name, passenger_id))
        connection.commit()
    except Exception as e:
        print("❌ Error", e)
    finally:
        connection.close()

def update_passenger_phone(passenger_id, new_phone):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE passengers SET phone = %s WHERE passenger_id = %s"
            cursor.execute(sql, (new_phone, passenger_id))
        connection.commit()
    except Exception as e:
        print("❌ Error", e)
    finally:
        connection.close()

def delete_passenger(passenger_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM passengers WHERE passenger_id = %s"
            cursor.execute(sql, (passenger_id,))
        connection.commit()
    except Exception as e:
        print("❌ Error", e)
    finally:
        connection.close()


def get_passenger_by_name(name):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
             query = "SELECT * FROM passengers WHERE name LIKE %s"
             cursor.execute(query, ('%' + name + '%'))
             result = cursor.fetchone()
             return result
    except Exception as e:
        print("❌ Error:", e)
        return []
    finally:
        connection.close()

def get_multiple_passengers(limit):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM passengers LIMIT %s"
                cursor.execute(query, (limit,))
                return cursor.fetchall()
        except Exception as e:
            print("❌ Error:", e)
            return []
        finally:
            connection.close()

def get_all_passengers():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
             query = "SELECT * FROM passengers"
             cursor.execute(query)                 
             return cursor.fetchall()
    except Exception as e:
        print("❌ Error:", e)
        return []
    finally:
        connection.close()

def get_passenger_by_id(passenger_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM passengers WHERE passenger_id = %s"
            cursor.execute(query, (passenger_id,))
            return cursor.fetchone()
    except Exception as e:
        print("❌ Error:", e)
    finally:
        connection.close()

