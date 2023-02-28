# Priravny dotaz na ziskani seznamu unikatnich dilu v cele databazi kusovniku. Vrati txt soubor se seznamem unikatnich dilu.

import os
import sqlite3
import time

# Urceni souboru a nazvu
current_folder_path = os.path.dirname(os.path.abspath(__file__))
database_name = 'programy.db'
database_path = f'{current_folder_path}\\{database_name}'
table_name = 'dilyXboudy'

### Ziskat unikatni dily v databazi

start_t = time.time()

print(f'Connecting to the database {database_name}.')

# Connect to database
conn = sqlite3.connect(database_path)

# Create cursor
cursor = conn.cursor()

print(f'Selecting all unique part numbers from table {table_name}.')

# Select all unique records (DISTINCT is for returning list of unique values)
cursor.execute(f'SELECT DISTINCT "part number" FROM "{table_name}"')

print(f'Query executed ...')

r = cursor.fetchall()

end1_t = time.time()

print(f'Query result fetched in {end1_t-start_t} seconds...')

# Close the connection
conn.close()

print(f'{len(r)} unikatnich PN nalezeno v tabulce {table_name} v databazi {database_name}.')

start_t = time.time()

# Writing list of uniques items into txt file output
with open(f'{current_folder_path}\\unique_pns_output.txt', 'w', encoding='UTF-8') as o:
    for pn in r:

        #print(pn)
        o.write(pn[0])
        o.write('\n')
    o.close()

end2_t = time.time()
print(f'List of unique part numbers from database {database_name} saved as txt file unique_pns_output.txt in current folder in {end2_t-start_t} seconds ...')

input(f'All done, press ENTER to exit program ...')
