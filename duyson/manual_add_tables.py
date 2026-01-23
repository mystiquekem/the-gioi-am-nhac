import sqlite3
conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()
table_creation_query = """
    CREATE TABLE Question (
        ID VARCHAR(255) NOT NULL PRIMARY KEY,
        QName VARCHAR(255) NOT NULL,
        CorrectA CHAR(25) NOT NULL,
        DecoyB CHAR(25) NOT NULL,
        DecoyC CHAR(25) NOT NULL,
        DecoyD CHAR(25) NOT NULL
    );
"""
cursor.execute(table_creation_query)
cursor.close()

