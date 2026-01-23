import sqlite3

# Connect to the database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Define the table name to be dropped
table_name = 'question'

try:
    # Execute the DROP TABLE statement with IF EXISTS
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    print(f"Table '{table_name}' dropped successfully (if it existed).")

    # Commit the changes
    conn.commit()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    conn.close()