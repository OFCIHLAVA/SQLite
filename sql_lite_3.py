import sqlite3

# 1. Connecting to / creating (if non existing yet) database
# Needs to establish connection to database

connection = sqlite3.connect("tutorial.db")

# prints connection object if one exists
print(connection) 

# 2. Creating cursor within the connection (worker object interacting with database)
cursor = con.cursor()

# 3. Creating tutorial table within database called movie

cursor.execute("CREATE TABLE movie(title, year, score)") 

# .execute makes cursor perform some action specified in brackets.
# CREATE TABLE is command for creating new table. UPPER case notation is standard for sql commands.
