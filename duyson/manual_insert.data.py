import sqlite3
conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()
cursor.execute("INSERT INTO Thesis VALUES ('62.21.02.02', 'Phạm Nghiêm Việt Anh', 'Âm nhạc học' , 'PGS.TS. Phạm Tú Hương' , 'Các tác phẩm hoà tấu thính phòng Việt Nam' ,'62.21.02.02.pdf')")
print("Data Inserted in the table: ")
cursor.execute("SELECT * FROM Thesis")
for row in cursor.fetchall():
    print(row)
conn.commit()
conn.close()

"""
class Thesis(db.Model):
    ID = db.Column(db.String(25), primary_key = True, nullable=False)
    Author = db.Column(db.String(25),nullable = False)
    Category = db.Column(db.String(25), nullable = False)
    Supervisor = db.Column(db.String(25), nullable = False)
    Name = db.Column(db.String(255),nullable = False)
    File_name = db.Column(db.String(25), nullable = False)

"""

