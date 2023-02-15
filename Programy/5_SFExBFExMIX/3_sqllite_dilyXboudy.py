# Vezme txt soubor vsech dilu z kusovniku pro kazdy priradi jeden zaznam pro kazdy finalni monument ve kterem se nachazi.
# Tyto zaznamy vlozi do zadane databaze, do zadane tabulky.
# V databazi, tabulce vzniknou zaznamy ve tvaru: dil_1 - monument1, dil_1 - monument2, dil_1 - monument3, , dil_2 - monument1, dil_2- monument1, , dil_3 - monument1  . . .

from Modules import sqllite, funkce_prace
import os
import time

# Urceni souboru a nazvu
current_folder_path = os.path.dirname(os.path.abspath(__file__))
database_name = 'programy_old.db'
database_path = f'{current_folder_path}\\{database_name}'
bom_update_file_path = f'{current_folder_path}\\CQ reporty\\update_kusovnik\\boudy_kusovnik.txt'

### BOM update preparation stuff from file

# Nacteni dat z CQ txt reportu
data = funkce_prace.import_kusovniku_LN(data_file)
# vytvoreni dvojic dil:monument na pridani do databaze
dily_monumenty_pridat = sqllite.get_pn_in_monuments(update_file_data)
# vzit tento seznam a updatovat databazi tabulku dilxbouda
sqllite.insert_many_records(database_path, "dilyXboudy", dily_monumenty_pridat)



print(f'polozky pridat vytvoreny.')
print(f'Jdu zapisovat.')

# with open(f'{current_folder_path}\\3 sql dil x boudy\\dilyVBoudach.txt', 'a', encoding='UTF-8') as o:
#     # Jump on new line at the end of the file
#     o.write('\n')
#     for i, line in enumerate(pridat_do_databaze):
#         print(i, line)
#         pn = line[0]
#         in_monument = line[-1]
#         o.write(f'{pn}\t{in_monument}\n')
#     o.close()    

input(f'copntinue')

### DATABAZE STUFF

# Otevreni txt zdrojoveho souboru pro nacteni dat. V souboru musi byt data pro kazdy record na samostatne lince, data v recordu od sebe oddelena TABulatorem. Kodovani txt souboru UTF-8.
# Na prvni lince musi byt zahlavi se jmeny sloupcu tak, jak budou v SQL databazi.

# with open(data_file_path, "r", encoding = "UTF-8") as f:
#     data = [tuple([field.strip() for field in line.split('\t')]) for line in f if line.strip()]
#     zahlavi_dat = data[0]
#     # Odstraneni zahlavi ze samotnych dat
#     data.pop(0)
#     print(f'Zahlavi souboru: {zahlavi_dat}')
#     print(f'Pocet radek v soubory s daty: {len(data)}')

# Delete some table by name if needed
# sqllite.delete_table(database_path, "dilyXboudy")

# Create table of Items and monuments in which these items are contained.
sqllite.create_table(database_path, 'dilyXboudy', f'"part number" TEXT NOT NULL, "obsazen v" TEXT NOT NULL')

# Print all tables in database programy and their records.
d_tables = sqllite.get_all_tables_in_database(database_path)
for t in d_tables:
    print(t)
    print(f'{sqllite.get_count_records_in_table(database_path, t)} records in table')
    # sqllite.show_all_records_database_in_table(database_path, t)
    # if t == "dilXbouda":
    #     # print all record lines
    #     sqllite.show_all_records_database_in_table(database_path, t)


# Ask user how many lines already processed
already_processed =  int(input(f'How many records already in database?  '))

start_time = time.time()
 
# Insert data from file for table itemsXmonuments into database one line at a time.
#sqllite.insert_records_into_database_into_table_from_file(database_path, 'dilyXboudy', data_file_path, "part number",already_processed)

# Insert data from file for table itemsXmonuments into database all lines in one go.
# sqllite.insert_many_records(database_path, "dilyXboudy", data)

# Create index on columns it table boudaXprogramy
# sqllite.create_index_on_column(database_path, "dilyXboudy", "part number")

# Vacuum the database
# sqllite.vacuum_database(database_path)

end_time = time.time()

trvani = end_time - start_time

print(f'start: {start_time}')
print(f'finished: {end_time}\n')
print(f'Time took: {trvani}')