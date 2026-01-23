import sqlite3
conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()
print("Data Inserted in the table: ")
cursor.execute("SELECT * FROM Question")
for row in cursor.fetchall():
    print(row)
conn.commit()
conn.close()