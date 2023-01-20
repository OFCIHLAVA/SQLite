import os
os.system('clear')

import sqlite3

# 1. Connecting to / creating (if non existing yet) database
# Needs to establish connection to database

connection = sqlite3.connect("tutorial.db")

# prints connection object if one exists
# print(connection) 

# 2. Creating cursor within the connection (worker object interacting with database)
cursor = connection.cursor()

# 3. Creating tutorial table within database called movie

# cursor.execute("CREATE TABLE movie(title, year, score)") 

# .execute makes cursor perform some action specified in brackets.
# CREATE TABLE is command for creating new table. UPPER case notation is standard for sql commands.

# To check, that table was created, we can inspect the sql_master table. 

result = cursor.execute("SELECT * FROM sqlite_master")
# print(result.fetchone())

# 4. Inserting some entrier into table

# cursor.execute("""
# 	INSERT INTO movie VALUES
# 		('Monthy Python and the Holy Grail', 1975, 8.2),
# 		('Paddington', 2017, 9.9)
# 		""")
# connection.commit()

# films = cursor.execute("SELECT score FROM movie")
# #or object in films:
# print(films.fetchall())

data = [
("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
("Monty Python's The Meaning of Life", 1983, 7.5),
("Monty Python's Life of Brian", 1979, 8.0),
]

# Inserting multiple entries from list of lines.
# Values contain ? for each data column in table inserting to.

# cursor.executemany("INSERT INTO movie VALUES(?,?,?)",data)
# connection.commit()

films = cursor.execute("SELECT year, title FROM movie ORDER BY year")
#or object in films:
# films = (films.fetchall())
# for film in films:
# 	print(film)

connection.close()

new_connection = sqlite3.connect("tutorial.db")
new_cursor = new_connection.cursor()
check_result = new_cursor.execute("SELECT title, year FROM movie ORDER BY score DESC")
title, year = check_result.fetchone()
print(check_result.fetchone())
print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')
print(check_result.fetchone())
print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')
print(check_result.fetchone())
print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')
print(check_result.fetchone())
print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')
print(check_result.fetchone())
print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')
for line in check_result:
	print(line)