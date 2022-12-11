# Import module
import sqlite3

# Connecting to sqlite
conn = sqlite3.connect('..\\Data\\gfg.db')

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

def create_db():
    try:
        table = '''CREATE TABLE ASSISTANT(SERIAL_NO INTEGER PRIMARY KEY,
                QUERY VARCHAR(255) NOT NULL ,
                DATE_TIME VARCHAR(50) NOT NULL );'''
        cursor.execute(table)
        return "SUCCESS"
    except sqlite3.OperationalError as e:
        return e # table ASSISTANT already exists

def add_data(query):
    table = "INSERT INTO ASSISTANT(QUERY, DATE_TIME) VALUES (?, datetime('now', 'localtime'))"
    cursor.execute(table, (query,))
    return True

def get_data():
    data = cursor.execute('SELECT * FROM ASSISTANT')
    table_head = []
    for column in data.description:
        table_head.append(column[0])
    print("{:<14} {:<49} {:<20}".format(table_head[0], table_head[1], table_head[2]))
    print()
    for row in data:
        print("{:<14} {:<49} {:<20}".format(row[0], row[1], row[2]))


add_data("get popular tv series")
get_data()