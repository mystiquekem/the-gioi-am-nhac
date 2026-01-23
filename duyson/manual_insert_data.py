import sqlite3
conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()
cursor.execute("INSERT INTO question VALUES ('05', '3+1', '5' , '2' , '3' ,'4')")
print("Data Inserted in the table: ")
cursor.execute("SELECT * FROM question")
for row in cursor.fetchall():
    print(row)
conn.commit()
conn.close()


