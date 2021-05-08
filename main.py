import pyodbc

def read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sites")
    for row in cursor:
        print(row)

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=hp;'
    'Database=iMediaDB;'
    'Trusted_Connection=yes;')

read(conn)