import pymysql

def get_connection():
    return pymysql.connect(
        host = "localhost",
        user = "root",
        password = "YOUR_PASS",       #enter your password here
        database = "airport_management_system",
        cursorclass = pymysql.cursors.DictCursor
    )
