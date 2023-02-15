# Vezme txt soubor vsech dilu z kusovniku pro kazdy priradi jeden zaznam pro kazdy finalni monument ve kterem se nachazi.
# Tyto zaznamy vlozi do zadane databaze, do zadane tabulky.
# V databazi, tabulce vzniknou zaznamy ve tvaru: dil_1 - monument1, dil_1 - monument2, dil_1 - monument3, , dil_2 - monument1, dil_2- monument1, , dil_3 - monument1  . . .

import sqlite3
import os
import time
from SQL_update.Modules import sqllite, funkce_prace

# Urceni souboru a nazvu
current_folder_path = os.path.dirname(os.path.abspath(__file__))
database_name = 'programy_old.db'
database_path = "Y:\\Departments\\Sales and Marketing\\Aftersales\\11_PLANNING\\23_Python_utilities\\5_SFExBFExMIX\\SQL_update\\programy_old.db"
# bom_update_file_path = f'{current_folder_path}\\CQ reporty\\update kusovniku\\boudy_kusovnik.txt'
# monumenty_update_file_path = f'{current_folder_path}\\1 sql boudy\\final monuments.txt'

######
# dily *** TBD **** - dodelat pozdeji, pokud bude potreba. zatim neni.
######

############
# dilyXboudy - Funkce pro správu tabulky databáze, kde jsou informace o tom, který díl se nachází ve kterých monumentech
############

## BOM update from file CQ BOM report
def update_database_bom_from_cq_file(database_path=str, cq_bom_file_path=str): # This will open the txt CQ bom file and add the items in it with their final monument to database programy, table dilyXboudy
    
    # Check if selected path is valid (not empty, is text file and there are some data in file)

    # Path leads to txt file → next check
    if is_txt_file(cq_bom_file_path):
        # File is not empty → process
        if not is_txt_file_empty((cq_bom_file_path)):
            # Nacteni dat z CQ txt reportu
            start_time = time.time()
            data = funkce_prace.import_kusovniku_LN(cq_bom_file_path)
            end_time = time.time()
            trvani = end_time - start_time
            # print(f'Data nactena z txt reportu CQ. Time took: {trvani}')

            # vytvoreni dvojic dil:monument na pridani do databaze
            start_time = time.time()
            dily_monumenty_pridat = sqllite.get_pn_in_monuments(data)
            end_time = time.time()
            trvani = end_time - start_time
            # print(f'Data pripravena ke vlozeni do databaze. Time took: {trvani}')

            # vzit tento seznam a updatovat databazi tabulku dilxbouda
            print(f'Vkladam data do databaze, this may take a while...')
            start_time = time.time()
            sqllite.insert_many_records(database_path, "dilyXboudy", dily_monumenty_pridat, [])
            end_time = time.time()
            trvani = end_time - start_time
            # print(f'Zaznamy vlozeny do databaze. Time took: {trvani}')

            # Nakonec:
            # A. vytvorit set pridavanych monumentu a pro kazdy proverit, jestli uz je v databazi monumentu a pokud jeste ne → pridat ho tam.
            # pridavane dily monumnetu jsou ve formatu (pn, monument)
            pridavane_monumenty = {pair[1] for pair in dily_monumenty_pridat}
            pridavane_monumenty = list(pridavane_monumenty)
            uz_drive_pridane_monumenty = check_if_monuments_in_database(database_path, pridavane_monumenty)

            # Creare result list of tupes of monuments and their default values to be added, which are not yet in database. (list of tuples needed for sql query inserting the records)
            final_monuments_pridat = [(m, "?", "?", "?") for m in pridavane_monumenty if m not in uz_drive_pridane_monumenty]

            # Insert these into database with default values        
            if final_monuments_pridat:
                # add monuments
                print(f'These monuments not yet in database → inserting: {final_monuments_pridat} with default values "?"')
                inserted_monuments = sqllite.insert_many_records(database_path, 'boudyXprogramy', final_monuments_pridat, [])
                print(inserted_monuments)

            # B. vytvorit set pridavanych part numberu a pro kazdy proverit, jestli uz je v databazi part numberu a pokud jeste ne → pridat ho tam.
            # pridavane dily monumnetu jsou ve formatu (pn, monument)
            pridavane_pns = {pair[0] for pair in dily_monumenty_pridat}
            pridavane_pns = list(pridavane_pns)
            uz_drive_pridane_pns = check_if_pns_in_database(database_path, pridavane_pns)

            # Creare result list of tuples of part numbers and their default values to be added, which are not yet in database. (list of tuples needed for sql query inserting the records)
            final_pns_pridat = [(pn, "?") for pn in pridavane_pns if pn not in uz_drive_pridane_pns]
            
            # Insert these into database with default values        
            if final_pns_pridat:
                # add pns
                print(f'These part numbers not yet in database → inserting: {final_pns_pridat} with default values "?"')
                inserted_pns = sqllite.insert_many_records(database_path, 'part_numbers', final_pns_pridat, ["part number"])
                print(inserted_pns)

            return f'OK - BOM Database succesfully updated. Time took: {round(trvani,2)}s.'
        return f'Warning! Selected .txt file is empty. Nothing to add...'
    return f'Warning! The selected filepath does not lead to a .txt file. Please, chose a different path...'

## BOM update from file txt pripravene sloupce dilTABv_monumentu
def update_database_bom_from_txt_list(database_path=str, txt_list_path=str): # This will open the txt file with list of itemXin_monument and add the items in it with their final monument to database programy, table dilyXboudy. Predpoklada se zahlavi na prvni lince v souboru.
    
    # Check if selected path is valid (not empty, is text file and there are some data in file)
    # Path leads to txt file → next check
    if is_txt_file(txt_list_path):
        # File is not empty → process
        if not is_txt_file_empty((txt_list_path)):
            # Nacteni txt souboru, kde jsou data k updatovani
            with open(txt_list_path, "r", encoding = "UTF-8") as f:
                dily_monumenty_pridat = [tuple([field.strip() for field in line.split('\t')]) for line in f if line.strip()]
                zahlavi_dat = dily_monumenty_pridat[0]
                # Odstraneni zahlavi ze samotnych dat
                dily_monumenty_pridat.pop(0)
                print(f'Zahlavi souboru: {zahlavi_dat}')
                print(f'Pocet radek v soubory s daty: {len(dily_monumenty_pridat)}')

                # Check, if data in file are valid. (each line has exactly 2 elements)
                for line in dily_monumenty_pridat:
                    if len(line) != 2:
                        return f'Warning! Data in selected file appears to have invalid format. Nothing added. Please check the file and try again...'

            # vzit tento seznam a updatovat databazi tabulku dilxbouda
            print(f'Vkladam data do databaze, this may take a while...')
            start_time = time.time()
            sqllite.insert_many_records(database_path, "dilyXboudy", dily_monumenty_pridat, [])
            end_time = time.time()
            trvani = end_time - start_time
            # print(f'Zaznamy vlozeny do databaze. Time took: {trvani}')

            # Nakonec:
            # A. vytvorit set pridavanych monumentu a pro kazdy proverit, jestli uz je v databazi monumentu a pokud jeste ne → pridat ho tam.
            # pridavane dily monumnetu jsou ve formatu (pn, monument)
            pridavane_monumenty = {pair[1] for pair in dily_monumenty_pridat}
            pridavane_monumenty = list(pridavane_monumenty)
            uz_drive_pridane_monumenty = check_if_monuments_in_database(database_path, pridavane_monumenty)

            # Creare result list of tupes of monuments and their default values to be added, which are not yet in database. (list of tuples needed for sql query inserting the records)
            final_monuments_pridat = [(m, "?", "?", "?") for m in pridavane_monumenty if m not in uz_drive_pridane_monumenty]

            # Insert these into database with default values        
            if final_monuments_pridat:
                # add monuments
                print(f'These monuments not yet in database → inserting: {final_monuments_pridat} with default values "?"')
                inserted_monuments = sqllite.insert_many_records(database_path, 'boudyXprogramy', final_monuments_pridat, [])
                print(inserted_monuments)

            # B. vytvorit set pridavanych part numberu a pro kazdy proverit, jestli uz je v databazi part numberu a pokud jeste ne → pridat ho tam.
            # pridavane dily monumnetu jsou ve formatu (pn, monument)
            pridavane_pns = {pair[0] for pair in dily_monumenty_pridat}
            pridavane_pns = list(pridavane_pns)
            uz_drive_pridane_pns = check_if_pns_in_database(database_path, pridavane_pns)

            # Creare result list of tuples of part numbers and their default values to be added, which are not yet in database. (list of tuples needed for sql query inserting the records)
            final_pns_pridat = [(pn, "?") for pn in pridavane_pns if pn not in uz_drive_pridane_pns]
            
            # Insert these into database with default values        
            if final_pns_pridat:
                # add pns
                print(f'These part numbers not yet in database → inserting: {final_pns_pridat} with default values "?"')
                inserted_pns = sqllite.insert_many_records(database_path, 'part_numbers', final_pns_pridat, ["part number"])
                print(inserted_pns)

            return f'OK - BOM Database succesfully updated. Time took: {round(trvani,2)}s.'
        return f'Warning! Selected .txt file is empty. Nothing to add...'
    return f'Warning! The selected filepath does not lead to a .txt file. Please, chose a different path...'

## BOM delete specific record

## Dodelat fci na smazani vech kontretnich boud / dilu. 
# - Pokud chceme smazat nejakou boudu, tak smazat vsechny pary v databazi, kde je bouda na druhe pozici paru.
# - Pokud chceme smazat nejaky dil, tak smazat vsechny pary v databazi, kde je dil na prvni pozici paru.

################
# boudyXprogramy - Funkce pro správu tabulky databáze, kde jsou informace o tom, který monument má jaký program a zda má monument nějaká speciální pravidla (napr. AFT comlpex Delta atd.)
################

## PROGRAMS add monuments from file / manualy

def add_monumnet(database_path=str, monument_values=list): # This will add one specific monument record into database.

    # Get column names in target table
    tcs = sqllite.get_table_columns(database_path, "boudyXprogramy")    
    
    # Isert given monument record
    sqllite.insert_record(database_path, "boudyXprogramy", tcs, monument_values)

def add_many_monumnets(database_path=str, monuments_to_add_file_path=str): # This will open the txt file with list of itemXin_monument and add the items in it with their final monument to database programy, table dilyXboudy. Predpoklada se zahlavi na prvni lince v souboru.
    # Check if selected path is valid (not empty, is text file and there are some data in file)
    # Path leads to txt file → next check
    if is_txt_file(monuments_to_add_file_path):
        # File is not empty → process
        if not is_txt_file_empty((monuments_to_add_file_path)):
            # Nacteni txt souboru, kde jsou data k updatovani
            with open(monuments_to_add_file_path, "r", encoding = "UTF-8") as f:
                monumenty_pridat = [tuple([field.strip() for field in line.split('\t')]) for line in f if line.strip()]
                zahlavi_dat = monumenty_pridat[0]
                # Odstraneni zahlavi ze samotnych dat
                monumenty_pridat.pop(0)
                print(f'Zahlavi souboru: {zahlavi_dat}')
                print(f'Pocet radek v soubory s daty: {len(monumenty_pridat)}')

                # Check, if data in file are valid. (each line has exactly 4 elements)
                for line in monumenty_pridat:
                    if len(line) != 4:
                        return f'Warning! Data in selected file appears to have invalid format. Nothing added. Please check the file and try again...'

            # vzit tento seznam a updatovat databazi tabulku monumentu
            print(f'Vkladam data do databaze, this may take a while...')
            start_time = time.time()
            sqllite.insert_many_records(database_path, "boudyXprogramy", monumenty_pridat, ["final monument"])
            end_time = time.time()
            trvani = end_time - start_time
            print(f'Zaznamy vlozeny do databaze. Time took: {trvani}')
            
            return f'OK - Monuments Database succesfully updated. Time took: {round(trvani,2)}s.'
        return f'Warning! Selected .txt file is empty. Nothing to add...'
    return f'Warning! The selected filepath does not lead to a .txt file. Please, chose a different path...'

## PROGRAMS update monuments from file / manualy

def update_monument(database_path=str, monument_to_update=str, updated_values=list): # Function to change single specific monument via GUI. (program / rules etc)
    
    # Get column names in target table
    tcs = sqllite.get_table_columns(database_path, "boudyXprogramy")

    # Update given record in database
    update_record(database_path, "boudyXprogramy", ["final monument"], monument_to_update, tcs, updated_values)
    
def update_many_monuments(database_path=str, update_file_path=str): # Function to change many monuments via GUI + txt file. (program / rules etc)
    
    # Path leads to txt file → next check
    if is_txt_file(cq_bom_file_path):
        # File is not empty → process
        if not is_txt_file_empty((cq_bom_file_path)):
            # Nacteni txt souboru, kde jsou data k updatovani
            with open(update_file_path, "r", encoding = "UTF-8") as f:
                monumenty_updatovat = [tuple([field.strip() for field in line.split('\t')]) for line in f if line.strip()]
                zahlavi_dat =monumenty_updatovat[0]

                # Odstraneni zahlavi ze samotnych dat
                monumenty_updatovat.pop(0)
                print(f'Zahlavi souboru: {zahlavi_dat}')
                print(f'Pocet radek v soubory s daty: {len(monumenty_updatovat)}')
                # print(data)

            # Get column names in target table
            tcs = sqllite.get_table_columns(database_path, "boudyXprogramy")

            # execute update many records based on txt file
            start_time = time.time()
            sqllite.update_many_records(database_path, "boudyXprogramy", ["final monument"], tcs, monumenty_updatovat)
            end_time = time.time()
            trvani = end_time - start_time

            return f'OK - Monuments Database succesfully updated. Time took: {round(trvani,2)}s.'
        return f'Warning! Selected .txt file is empty. Nothing to add...'
    return f'Warning! The selected filepath does not lead to a .txt file. Please, chose a different path...'

## PROGRAMS delete from file / manualy

def delete_monument(database_path=str,  monument_to_delete=str): # Function to delete 1 specified monument from database.
    
    # Make list from monument to delete
    m_list = [monument_to_delete] # (required by get spec record function)

    # Delete specified monumnet
    sqllite.delete_records(database_path, "boudyXprogramy", ["final monument"], m_list)

def delete_many_monuments(database_path=str, delete_monuments_file_path=str): # Function to delete many monuments from database, monuments specified in txt file.
    
    # Path leads to txt file → next check
    if is_txt_file(delete_monuments_file_path):
        # File is not empty → process
        if not is_txt_file_empty((delete_monuments_file_path)):
            # Nacteni txt souboru, kde jsou data k deletovani
            with open(delete_monuments_file_path, "r", encoding = "UTF-8") as f:
                monumenty_delete = [tuple([field.strip().replace("\n", "").replace(" ", "") for field in line.split('\t')]) for line in f if line.strip()]
                zahlavi_dat = monumenty_delete[0]

            # Check, if data in file are valid. (each line has exactly 1 element - monument to delete)
            for line in monumenty_delete:
                if len(line) != 1:
                    return f'Warning! Data in selected file appears to have invalid format. Nothing added. Please check the file and try again...'    

            # Odstraneni zahlavi ze samotnych dat
            monumenty_delete.pop(0)
            print(f'Zahlavi souboru: {zahlavi_dat}')
            print(f'Pocet radek v soubory s daty: {len(monumenty_delete)}')
            # print(data)

            # Delete specified monuments AND their BOM records
            start_time = time.time()            
            # Deleting monuments
            deleted_monuments = sqllite.delete_many_records(database_path, "boudyXprogramy", ["final monument"], monumenty_delete)
            # Deleting their BOM records
            if deleted_monuments:            
                deleted_monuments_bom_pairs = sqllite.delete_many_records(database_path, "dilyXboudy", ["obsazen v"], monumenty_delete)
            end_time = time.time()
            trvani = end_time - start_time            
            
            if not deleted_monuments:
                return f'WARNING! No record matches given criteria → Nothing deleted.'
            
            return f'OK - Monuments {len(deleted_monuments)} succesfully deleted.\nAlso deletem BOM database records for these monuments\nTime took: {round(trvani,2)}s.'
        return f'Warning! Selected .txt file is empty. Nothing to delete...'
    return f'Warning! The selected filepath does not lead to a .txt file. Please, chose a different path...'


################
# OSTATNÍ FUNKCE
################

def uklidit_databazi(database_path=str): # Function to rebuild and clean database. Use after major changes / updates to database file. This clean the database.
    
    # Vacuum database
    print(f'Uklizim v databazi po upravach, this may take a while...')
    start_time = time.time()
    sqllite.vacuum_database(database_path)
    end_time = time.time()
    trvani = end_time - start_time
    print(f'Databaze vyluxovana. Time took: {trvani}')

def find_monument(database_path=str, monument_to_find=str):
    # 1. Find the record to update
    # make list from inputed monumnet
    m_list = [monument_to_find] # (required by get spec record function)
    
    # Get record to be u[dated from database
    record_to_update = sqllite.get_specific_record(database_path, "boudyXprogramy", ["final monument"], m_list)[0] # Returns list of tuples 
    rowid = record_to_update[0]
    monument_pn = record_to_update[1]
    monument_desc = record_to_update[2]
    monument_program = record_to_update[3]
    monument_rules = record_to_update[4]
    #print(rowid, monument_pn, monument_desc, monument_program, monument_rules)
    return rowid, monument_pn, monument_desc, monument_program, monument_rules

def find_pn_in_monument(database_path=str, pn_to_search_for=str, monument_to_search_for=str):

    # make list from inputed monumnet
    pn_monument_list = [pn_to_search_for, monument_to_search_for] # (required by get spec record function)
    print(f'zadani:{pn_monument_list}')

    # Get record from the database
    record = sqllite.get_specific_record(database_path, "dilyXboudy", ["part number", "obsazen v"], pn_monument_list) # Returns list of tuples 
    print(record)

    # If such record not found → return None
    if not record:
        return

    # If record found, return it, take tupple from it and return it
    record = record[0]
    
    rowid = record[0]
    pn = record[1]
    in_monument = record[2]

    #print(rowid, monument_pn, monument_desc, monument_program, monument_rules)
    return rowid, pn, in_monument 

def is_txt_file(path=str): # Checks given path, if it is txt file. Returns True/False
    # First replace new line character in path to clean it
    return True if path.replace("\n","").endswith(".txt") else False

def is_txt_file_empty(path=str): # Checks given path, if it is txt file, checks, if there are some data in it. Returns True/False
    with open(path, 'r', encoding='UTF-8') as file:
        if not file.read().strip():
            return True
        else:
            return False

def check_if_monuments_in_database(database_path=str, monuments_to_find=list): # Function checks if monuments from given set already in given table in given database. Returns list list of monuments already in database.

    # Connect to database
    conn = sqlite3.connect(database_path)

    # Cursor
    cursor = conn.cursor()

    # Create placeholder str
    placeholders = ",".join(["?" for m in monuments_to_find])

    # Creare SQL statement to find all the monuments from set
    query = f'SELECT "final monument" FROM "boudyXprogramy" WHERE "final monument" IN ({placeholders})'

    # Run the query
    cursor.execute(query, monuments_to_find)
    result = cursor.fetchall()

    if not result:
        print(f'No monumets from given list are yet in database.')
        return
    else:
        #Create result list
        monuments_already_in_database = [r[0] for r in result]
        #print(f'monumenty already in database:')
        #for m in monuments_already_in_database:
        #    print(m)
        
        return monuments_already_in_database

def check_if_pns_in_database(database_path=str, pns_to_find=list): # Function checks if part numbers from given set already in given table in given database. Returns list list of part numbers already in database.

    # Connect to database
    conn = sqlite3.connect(database_path)

    # Cursor
    cursor = conn.cursor()

    # Create placeholder str
    placeholders = ",".join(["?" for m in pns_to_find])

    # Creare SQL statement to find all the pns from set
    query = f'SELECT "final monument" FROM "part_numbers" WHERE "part number" IN ({placeholders})'

    # Run the query
    cursor.execute(query, pns_to_find)
    result = cursor.fetchall()

    if not result:
        print(f'No part numbers from given list are yet in database.')
        return
    else:
        #Create result list
        pns_already_in_database = [r[0] for r in result]       
        return pns_already_in_database