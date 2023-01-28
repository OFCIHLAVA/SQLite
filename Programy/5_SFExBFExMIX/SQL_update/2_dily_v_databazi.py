# Vezme txt soubor vsech unikatnich dilu ziskanych pomoci dotazu q1 unikatni dily v databazi a jejich description ze stejneho souboru, vytvori zaznam pro kazdy dil.
# Tyto zaznamy vlozi do zadane databaze, do zadane tabulky.
# V databazi, tabulce vzniknou zaznamy ve tvaru: dil_1 - decription_1, dil_2 - decription_2, ...

from Modules import sqllite
import os
import time

### Urceni souboru a nazvu

# Nalezeni stavajiciho umisteni
current_folder_path = os.path.dirname(os.path.abspath(__file__))
# Nazev databaze, kam chceme vkladat zaznamy
database_name = 'programy.db'
# Sestaveni cesty databaze (predpoklada, ze se databaze nachazi ve stejne slozce.)
database_path = f'{current_folder_path}\\{database_name}'
# Sestaveni cesty import filu (predpoklada, ze se file nachazi v podslozce 2 sql dily.)
data_file_path = f'{current_folder_path}\\2 sql dily\\unique_pns_output.txt'

# Otevreni txt zdrojoveho souboru pro nacteni dat. V souboru musi byt data pro kazdy record na samostatne lince, data v recordu od sebe oddelena TABulatorem. Kodovani txt souboru UTF-8.
# Na prvni lince musi byt zahlavi se jmeny sloupcu tak, jak budou v SQL databazi.

with open(data_file_path, "r", encoding = "UTF-8") as f:
    data = [tuple([field.strip() for field in line.split('\t')]) for line in f if line.strip()]
    zahlavi_dat = data[0]
    # Odstraneni zahlavi ze samotnych dat
    data.pop(0)
    print(f'Zahlavi souboru: {zahlavi_dat}')
    print(f'Pocet radek v soubory s daty: {len(data)}')

# Create table of Part numbers and their description.
sqllite.create_table(database_path, 'part_numbers', f'"part number" TEXT NOT NULL, "description" TEXT NOT NULL')
# Print all tables in database programy and their records.
d_tables = sqllite.get_all_tables_in_database(database_path)
print(d_tables)
for t in d_tables:
    print(t)
    # show count of records in each table
    sqllite.get_count_records_in_table(database_path, t)    
    # if t == "part_numbers":
    #     # print all record lines
    #     sqllite.show_all_records_database_in_table(database_path, t)

# Delete some table by name if needed
# sqllite.delete_table(database_path, "part numbers")

# Ask user how many lines already processed
already_processed =  int(input(f'How many records already in database?  '))

start_time = time.time()
 
# Insert data from file for table itemsXmonuments into database one line at a time.
# sqllite.insert_records_into_database_into_table_from_file(database_path, 'part_numbers', data_file_path, "part number", already_processed)

# Insert data from file for selected table into database all lines in one go.
# sqllite.insert_many_(database_path, 'part_numbers', data)

end_time = time.time()

trvani = end_time - start_time

print(f'start: {start_time}')
print(f'finished: {end_time}\n')
print(f'Time took: {trvani}')