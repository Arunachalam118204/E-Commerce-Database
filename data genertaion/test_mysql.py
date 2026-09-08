import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="e_commerce"
    )

    print("Connected to MySQL successfully!")

    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE()")

    result = cursor.fetchone()

    print("Current database:", result[0])

    cursor.close()
    conn.close()

    print("Connection closed successfully!")

except mysql.connector.Error as e:
    print("MySQL ERROR:")
    print(e)