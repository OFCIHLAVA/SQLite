# Vezme txt soubor vsech finalnich monumentů a přiřadí jim název, program a případně informaci o speciálních podmínkách.
# Tyto zaznamy vlozi do zadane databaze, do zadane tabulky.
# V databazi, tabulce vzniknou zaznamy ve tvaru: monument1 - decription_m1 - program_m1, monument2 - decription_m2 - program_m2, ...

from Modules import sqllite
import os
import time

# Urceni souboru a nazvu
current_folder_path = os.path.dirname(os.path.abspath(__file__))
database_name = 'programy.db'
database_path = f'{current_folder_path}\\{database_name}'
data_file_path = f'{current_folder_path}\\1 sql boudy\\final monuments.txt'

# Otevreni txt zdrojoveho souboru pro nacteni dat. V souboru musi byt data pro kazdy record na samostatne lince, data v recordu od sebe oddelena TABulatorem. Kodovani txt souboru UTF-8.
# Na prvni lince musi byt zahlavi se jmeny sloupcu tak, jak budou v SQL databazi.

with open(data_file_path, "r", encoding = "UTF-8") as f:
    data = [tuple([field.strip() for field in line.split('\t')]) for line in f if line.strip()]
    zahlavi_dat = data[0]
    # Odstraneni zahlavi ze samotnych dat
    data.pop(0)
    print(f'Zahlavi souboru: {zahlavi_dat}')
    print(f'Pocet radek v soubory s daty: {len(data)}')

input()

# Create table of Items and monuments in which these items are contained.
sqllite.create_table(database_path, 'boudyXprogramy', f'"final monument" TEXT NOT NULL, "description" TEXT NOT NULL, "program" TEXT NOT NULL, "specific rules" TEXT NOT NULL')
# Print all tables in database programy and their records.
d_tables = sqllite.get_all_tables_in_database(database_path)
for t in d_tables:
    print(t)
    if t == 'boudyXprogramy':
        sqllite.show_all_records_database_in_table(database_path, t)

# Ask user how many lines already processed
already_processed =  int(input(f'How many records already in database?  '))

start_time = time.time()
 
# Insert data from file for table itemsXmonuments into database one line at a time.
#sqllite.insert_records_into_database_into_table_from_file(database_path, 'dilyXboudy', data_file_path, "part number",already_processed )

# Insert data from file for selectred table into database all lines in one go.
# sqllite.insert_many_items(database_path, 'boudyXprogramy', data)

end_time = time.time()

trvani = end_time - start_time

print(f'start: {start_time}')
print(f'finished: {end_time}\n')
print(f'Time took: {trvani}')