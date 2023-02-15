# Module with SQLlite database management functions.

import sqlite3
import os

def create_table(database=str, table_name=str, columns_statement=str): # Functin to create / conect database with specified table with specified columns.
                                                             # columns_statement parameter needs to be string with SQL statement as when creating table in sql.
                                                             # for example: 'name TEXT NOT NULL, age INTEGER NOT NULL' 
    # Check if the database file exists
    if not os.path.exists(database):
        print(f"Database '{database}' does not exist. Creating database file '{database}' now.")
    else:
        print(f"Database '{database}' already exists. Connecting to the database file.")

    try:
        # Connect to the database
        conn = sqlite3.connect(database)

        # Create a cursor
        cursor = conn.cursor()

        # Check if the table already exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = cursor.fetchone()
        if result:
            print(f"Table '{table_name}' already exists in database '{database}', not creating new table.")
        else:
            # Create the table
            cursor.execute(f'CREATE TABLE {table_name} ({columns_statement})')
            print(f'Table {table_name} created in database {database}')

        # Save the changes
        conn.commit()
    except sqlite3.OperationalError as e:
        # The database does not exist
        if "no such table" in str(e):
            print(f"Database '{database}' does not exist")
        else:
            print(f'Error when connectiong to the database: {e}.')
    except Exception as e:
        print(f'Error when connectiong to the database: {e}')
    finally:
        # Close the connection
        conn.close()

def get_all_tables_in_database(database=str):        
    # print(f'Showing all table names in database: {database}:\n')
    # Connect to the database
    conn = sqlite3.connect(database)
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Execute a SELECT statement to retrieve the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    # Get the list of tables
    tables = [row[0] for row in cursor]
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return tables

def get_table_columns(database=str, table_name=str): # Returns list of columns names.

    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Retrieve the column names for the materials table
    cursor.execute(f'PRAGMA table_info({table_name})')

    # Store the column names in a list
    column_names = [row[1] for row in cursor if row[1] != "id"]

    # Close the connection
    conn.close()
    return column_names    

def get_count_records_in_table(database=str, table_name=str): # Returns number of lines of records in specified table in specified database.
    
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Return count of records in table, we want to delete
    cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')

    # Result of fech is tupple with count of lines at 0th index.
    r = cursor.fetchone()
    count = r[0]
    
    print(f'There are no records in table: "{table_name}".') if count == 0 else print(f'There are {count} records in table "{table_name}".')
    
    # Close the connection
    conn.close()

    return count

def show_all_records_database_in_table(database=str, table_name=str): # Shows all lines in given database and table with its headings.
    
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Retrieve the column names for table
    column_names = get_table_columns(database, f'"{table_name}"')

    # Select all rows from the materials table
    cursor.execute(f'SELECT rowid, * FROM "{table_name}"')
    # Print count of records
    rows = cursor.fetchall()
    print(f'{len(rows)} records in database {database}, table {table_name}:\n')

    # Print the records
    print(f'Showing records in database: {database}, in table: {table_name}.\n')    

    # Adding ID colum name to column names (optional)
    # column_names.insert(0, "ID")

    # Print the column headings
    print('\t'.join(column_names))

    # Iterate over the result set and print the rows

    for row in rows:
        print('\t'.join([str(x) for x in row]))

    # Close the connection
    conn.close()

def insert_records_into_database_into_table_from_file(database=str, table_name=str, filename=str, uniques_id_column_name=str, count_already_processed_file_lines=int, unique_items=bool):  # Funtion to load data from txt. file and insert them. If want to keep unique items, unique items → TRUE else False (vlozi vsechny linky ze souboru)
                                                                                                        # into coresponding table in database.
    
    print(f'Inserting records from file {filename} into table {table_name} in database {database}, primary key = {uniques_id_column_name}')

    # Get column names of table records are being inserted into
    print(f'getting column names of destination table...')
    table_column_names = get_table_columns(database, table_name)
    print(f'Columns in destination table: {", ".join(table_column_names)}')

    # Open the text file for reading, specifying the encoding
    print(f'Opening file {filename}...')
    with open(filename, 'r', encoding='utf-8') as f:    
        print(f'Opening the import file to get number of records to insert into database ...')
        # Number of lines in text
        count_lines = len(f.readlines())
        print(f'Done. Number of records to be inserted into database: {count_lines}.')
        f.close()     

    # Open the text file for reading, specifying the encoding
    print(f'Opening file {filename}...')
    with open(filename, 'r', encoding='utf-8') as f: 
        print(f'Opening the import file to insert records into database ...')
        # Finding the headings and matching it to columns in destination table

        # Find the first non empty line of the file
        for line in f:            
            # Skip blank lines
            if not line.strip():
                continue            
            # Take first text line as headings and convert them to lower case
            headings_line = line
            headings = line.strip().split('\t')
            headings = [heading.lower() for heading in headings]
            
            print(f'Headings of the file: {", ".join(headings)}')
            break

        # Find the indices of the heading from file to corespond the column names in destination table. Creates set of tuples
        # from headings in format (heading index, heading) to corespond destination table column names.
        headings_indeces = list()
        for column_name in table_column_names:
            for i, heading in enumerate(headings):
                if heading == column_name.lower():
                    headings_indeces.append((i, heading))
        print(f'For column names in destanition table: {table_column_names}, I have found corresponding data columns in upload file:')
        for h_index in headings_indeces:
            column_name =  h_index[1]
            column_index_in_file = h_index[0]+1
            print(f'Column name: {column_name}, column nr. {column_index_in_file}.')
                    
        # Find the field which identifies unique items in destination table
        for h_index in headings_indeces:
            if h_index[1] == uniques_id_column_name:
                unique_item_index = h_index[0]
                break
        print(f'Unique records indentifier: {uniques_id_column_name} found in column: {unique_item_index+1} in upload file.')        
   
        # Inserting data in table

        print(f'Connecting to the database...')    
        # Connecting to the database
        conn = sqlite3.connect(database)

        # Progress counter
        processed_lines = 0
        progress = 0

        # File Lines counter
        line_nr = 0

        # Read each subsequent line of the file 
        for line in f:
            # Skip blank lines
            if not line.strip():
                continue
            
            # Skips over headings line to first line of data
            if line == headings_line:
                continue
            
            # Lines counter
            line_nr+=1
            # Only insert line if not already inserted into database earlier
            if count_already_processed_file_lines >= line_nr:
                # print(f'nevkladam')
                continue
            else:            
                # print(f'vkladam {line}')
                # Split the line into fields using a tab character as the separator
                fields = line.strip().split('\t')            
                item = fields[unique_item_index]
                # print(f'Item to insert: {item}, Values to insert for that item: {fields}.')

                # # Extract the part number and description from the fields
                # part_number = fields[part_number_index]
                # description = fields[description_index]

                # Find the coresponding values from len to insert into table
                # for h in headings_indeces:
                #     print(h)
                item_values = [fields[h[0]] for h in headings_indeces]
                # print(f'Values to be insert to table for this item: {item_values}')

                ## A] IF we want to have only one record for each unique item (TRUE in last parameter) → will update records, if not same as in import file
                if unique_items == True:
                    # Check if the item already exists in the table
                    print(f'Checking if item {item} already exists in database.')
                    if not item_exists(database, table_name, headings[unique_item_index], item):
                        print(f'Item {item} no found in table: {table_name} in database {database}.')
                        # Insert the item into the table            
                        insert_record(database, table_name, table_column_names, item_values)

                    else:
                        print(f'Item {item} already found in table: {table_name} in database {database}.')
                        print(f'Checking, if record for item {item} in table: {table_name} in database {database} is the same as in upload file.')
                        if not record_is_same(database, table_name, headings[unique_item_index], item, table_column_names, item_values):
                            print(f'Record is not the same, updating item in database with data from upload file.')  
                            update_record(database, table_name, headings[unique_item_index], item, table_column_names, item_values)
                        else:
                            print(f'Record is the same, skipping to next line in upload file.')        
                else:
                    ## B] IF we want to insert each line from the file without checking, in item beeing inserted is already in datrabase. (will produce multiple records for each unique item)
                        # Insert the item into the table            
                        insert_record(database, table_name, table_column_names, item_values)
                processed_lines += 1

                # progres print    

                # if round((processed_lines+count_already_processed) / count_lines, 3) > progress:
                progress = round((processed_lines+count_already_processed_file_lines) / count_lines, 3)
                print(f'Zpracovano linek: {processed_lines+count_already_processed_file_lines} / {count_lines}\t{progress} %')  


        # Close the connection
        conn.close()            

def insert_record(database=str, table_name=str, table_columns=list, item_values=list): # Function to insert new item into the table. values order must match the table_columns order.
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Insert the new item into the table
        
    # Destinations columns SQL clause str
    columns_str = ", ".join((f'"{t_c}"' for t_c in table_columns))
    # print(columns_str)

    # Values placeholdesr str
    placeholders = ", ".join(["?" for c in table_columns])
    # print(placeholders)

    # Values to be inserted for record (must be is same order as column order)
    # print(item_values)

    # Insert into table
    cursor.execute(f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})', tuple(item_values))

    # print(f'Record succesfully inserted into database:')
    # Check the newly added record
    
    # Last added record rowid
    last_added_row_id = cursor.lastrowid
    # print(f'posledni pridane id: {last_added_row_id}')

    cursor.execute(f'SELECT rowid, * FROM {table_name} WHERE rowid={last_added_row_id}')
    result = cursor.fetchone()
    print(f'Kontrola posleniho pridaneho zaznamu:')
    print(result)

    # Save the changes
    conn.commit()

    # Close the connection
    conn.close()

    return result

def insert_many_records(database=str, table_name=str, records_values=list, overwrite_by_columns=list): # Function to insert multiple new records into the table.
    # Records values is a list of tuples, where order of vaules in tuples must match the table_columns order. Will not add record if identic record already in table.
    # Optionaly can be passed list of columns. In that case, will check, if newly added record has same values in these columns with any record already in the table. 
    # If yes → will consider the record in table as the same as one being added, and will update record already in database to match the added record. (This is for overwriting old records with nwe values)
    
    # Get column names of table records are being inserted into
    #print(f'getting column names of destination table...')
    table_column_names = get_table_columns(database, table_name)
    #print(f'Columns in destination table: {", ".join(table_column_names)}')

    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Insert the new item into the table
        
    # Destinations columns SQL clause str
    columns_str = ", ".join((f'"{t_c}"' for t_c in table_column_names))
    #print(columns_str)

    # Values placeholdesr str
    placeholders = ", ".join(["?" for c in table_column_names])
    #print(placeholders)
    
    # Duplicate reocrd check - Mandatory
    # Create the WHERE clause of the SQL statement to select columns from table in database to compare with criteria provided.
    column_values_to_select_str = "=? AND ".join([f'"{name}"' for name in table_column_names])

    # Overwrite existing record check - Optional
    # Create the SQL statement to check if record from optional list already in database
    overwrite_by_columns_to_select_str = "=? AND ".join([f'"{name}"' for name in overwrite_by_columns])
    values_to_overwrite_by_indexes = [table_column_names.index(c) for c in overwrite_by_columns]

    # Insert into table
    # cursor.executemany(f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})', records_values)
    for record in records_values:
        #print(record)
        # Check if such record already in database
        #print(f'Kontroluju zda je stejny record uz v databazi.')
        cursor.execute(f'SELECT rowid, * FROM "{table_name}" WHERE {column_values_to_select_str}=?', record)
        exists = cursor.fetchall()
        if exists:
            #print(f'Record {table_column_names}:{record} already exists in database, skipping to next record.')
            continue
        # if not, check if some records to ocverwrite
        elif overwrite_by_columns:
            #print(f'Record {table_column_names}:{record} not yet in database. Proceedning to the next check.')
            # If so , try find any matching records already in table
            values_to_check = [record[i] for i in values_to_overwrite_by_indexes]
            #print(f'Kontroluji, jestli je potreba updatovat record uz v databazi pro vkladany record: {record}')
            #print(f'Hledam shodu ve sloupcich: {overwrite_by_columns_to_select_str}, hledam hodnoty: {values_to_check}')
            values_to_check=tuple(values_to_check)
            #print(f'SQL statement na kontrolu shody:')
            #print(f'SELECT rowid, * FROM "{table_name}" WHERE {overwrite_by_columns_to_select_str}=?')
            cursor.execute(f'SELECT rowid, * FROM "{table_name}" WHERE {overwrite_by_columns_to_select_str}=?', values_to_check)    
            exists = cursor.fetchall()
            #print(exists)
            # If any found → overwrite them
            if exists:
                #print(f'record with such parameters found, updating wiht new values')
                values_with_where_values_at_end = [v for v in record] + list(values_to_check)
                #print(f'Values for the UPDATE sql statement: {values_with_where_values_at_end}')
                #print(f'SQL update statmenet:')
                #print(f'UPDATE "{table_name}" SET {column_values_to_select_str}=? WHERE {overwrite_by_columns_to_select_str}=?')
                cursor.execute(f'UPDATE "{table_name}" SET {column_values_to_select_str}=? WHERE {overwrite_by_columns_to_select_str}=?', tuple(values_with_where_values_at_end))
            # Else, just insert record
            else:       
                #print(f'Record {table_column_names}:{record} not yet in database, adding record.') 
                try:
                    #print(f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})')
                    cursor.execute(f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})', record)
                except:                    
                    print(f'Error: {record}') 
        # Else just insert new record
        else:       
            #print(f'Record {table_column_names}:{record} not yet in database, adding record.') 
            try:
                cursor.execute(f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})', record)
            except:
                print(f'Error: {record}') 

    print(f'Records succesfully inserted into database: {database}')

    # Save the changes
    conn.commit()
    # Close the connection
    conn.close()

def item_exists(database=str, table_name=str, item_column_name=str ,item=str): # Function to check, if item is already in table
    
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Execute a SELECT statement to check if the item already exists
    cursor.execute(f'SELECT * FROM "{table_name}" WHERE "{item_column_name}"=?', (item,))

    # Check if the SELECT statement returned any rows
    exists = cursor.fetchone() is not None

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return exists

def get_specific_record(database=str, table_name=str, table_columns=list, item_values=list): # Function to get specific record/records from database based on criteria passed to function. Provide list of columns and list of values for therse columns.
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Execute a SELECT statement for record based on criteria provided  
    
    # Create the WHERE clause of the SQL statement to select columns from table in database to compare with criteria provided.
    column_values_to_select_str = "=? AND ".join([f'"{name}"' for name in table_columns])
    # print(column_values_to_select_str)

    # Create the SELECT statement
    cursor.execute(f'SELECT rowid, * FROM "{table_name}" WHERE {column_values_to_select_str}=?', tuple(item_values))
    print(f'SELECT rowid, * FROM "{table_name}" WHERE {column_values_to_select_str}=?', tuple(item_values))

    # Fetch result of the query
    result = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return result

def record_is_same(database=str, table_name=str, item_column_name=str ,item=str, table_column_names= list, item_values=list): # Function to check, if material is already in table and its description is the same
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Execute a SELECT statement to check if the item in table already exists    
    
    # Create the WHERE clause of the SQL statement to select columns from table in database to compare with input record.
    column_values_to_check_str = "=? AND ".join([name for name in table_column_names if name != item_column_name])
    # print(column_values_to_check_str)
    
    # Moving the item value on first position in values so it coresponds the order of sql statement in query.
    item_values.remove(item)
    # print(item_values, type(item_values))
    item_values.insert(0, item)
    # print(item_values, type(item_values))

    cursor.execute(f'SELECT * FROM "{table_name}" WHERE "{item_column_name}"=? AND {column_values_to_check_str}=?', tuple(item_values))

    # Check if the SELECT statement returned any rows
    exists = cursor.fetchone() is not None

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return exists

def update_record(database=str, table_name=str, item_column_name=str, item=str, table_column_names=list, item_values=list): # Updates values of records for existing item in database - Function to update values of item already found in table, if same item with different values is beeing added to table
    print(f'Updating record...')
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Update item with new values provided

    #print(f'Table columns: {table_column_names}')
    # Create the SET SQL str statement (what columns we want to update in format x=?, y=? ...)    
    set_columns_str = "=?, ".join(f'"{t_c}"' for t_c in table_column_names)
    # print(f'SQL statement for SET columns to be updated:')
    # print(set_columns_str)

    # Add the item variable for the WHERE clause of SQL statement at the end of the list of new values, so that list matches the order of columns being updated.
    # print(f'List of new values without the WHERE item:')
    # print(item_values)
    item_values.append(item)
    # print(f'List of new values with the WHERE item added at the end:')
    # print(item_values)

    # Check what records will be updated
    cursor.execute(f'SELECT rowid, * FROM "{table_name}" WHERE "{item_column_name}"="{item}"')
    result = cursor.fetchall()
    print(f'Records to be updated: {result}')
    row_ids_od_records_to_be_changed = [str(record[0]) for record in result]
    print(row_ids_od_records_to_be_changed)

    print(f'UPDATE "{table_name}" SET {set_columns_str}=? WHERE "{item_column_name}"=?', tuple(item_values))   
    cursor.execute(f'UPDATE "{table_name}" SET {set_columns_str}=? WHERE "{item_column_name}"=?', tuple(item_values))
    # Commit the transaction
    conn.commit()

    # Check the records afer update
    str_row_ids = ",".join(row_ids_od_records_to_be_changed)
    cursor.execute(f'SELECT rowid, * FROM "{table_name}" WHERE rowid IN ({str_row_ids})')
    result = cursor.fetchall()
    print(f'Updated records: {result}')

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # return updated records
    return result

def update_many_records(database=str, table_name=str, item_column_name=str, item=str, table_column_names=list, items_values_list=list): # Updates values of records for existing items in database - Function to update values of items already found in table, if same item with different values is beeing added to table
    
    ### NOT WORKING PROPERLY - NEEDS TO BE REDESIGNED WHEN NEEDED
    
    print(f'Updating many records...')
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Update item with new values provided

    # Create the SET SQL str statement (what columns we want to update in format x=?, y=? ...)    
    set_columns_str = "=?, ".join(f'"{t_c}"' for t_c in table_column_names)

    # for each record values list in input list, add the item at the end of the list, so that it corresponds with the SQL statemnet with WHERE clause. Then transform each values list into tuple for better sql performance.
    for i, rv in enumerate(items_values_list):
        # find what inex have the comlumn of item beeing updated
        index_where_column = table_column_names.index(item_column_name)        
        item = rv[index_where_column]        
        items_values_list[i] = tuple(rv.append(item))        

    # print(f'UPDATE "{table_name}" SET {set_columns_str}=? WHERE "{item_column_name}"=?', tuple(item_values))   
    cursor.executemany(f'UPDATE "{table_name}" SET {set_columns_str}=? WHERE "{item_column_name}"=?', items_values_list)
    
    # Commit the transaction
    conn.commit()

    # print how many records updated
    print(f'Records updated succesfully')
    print(f'Count updated records: {len(items_values_list)}')

    # Close the cursor and connection
    cursor.close()
    conn.close()

def delete_table(database=str, table_name=str): # Deletes specified table from specified database, if such table in in.

    # Connectiong to database
    conn = sqlite3.connect(database)
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Execute a SELECT statement to check if requested table exists in database
    cursor.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name= "{table_name}"')
    r = cursor.fetchall()

    # If such table not in database, return error
    if not r:
        print(f'No such table with name: {table_name} found in database {database}. Cannot delete table.')
        return

    # Get number of records i table in database
    n = get_count_records_in_table(database, table_name)

    # Ask user confirmation of deleting table
    print(f'Are you sure, you want to delete teble: {table_name} from database {database}?\nThis cannot be undode, all records in table will be lost.')
    i = ""
    while i not in ["e", "s"]:
        i=input(f'Confirm D[E]leting or [S]torno Deleting :').lower()

    print(i)
    # End deletion, if Storned by user
    if i == "s":
        print(f'Deletion aborted by user. Table {table_name} remains unchanged in database.')
        return 
    
    # Else, drop table from database
    cursor.execute(f'DROP TABLE "{table_name}"')

    # Commint the changes to database
    conn.commit()
    print(f'Table {table_name} succesfully deleted from database {database}')

    # Close the connection
    conn.close()

def delete_record(database=str, table_name=str, table_column_names=list, item_values=list): # Deletes record from table where record values matches the condition specified.
    # Connect to database
    conn = sqlite3.connect(database)

    # Create cursor
    cursor = conn.cursor()

    # Create the WHERE clause of the SQL statement to select columns from table in database to compare with criteria provided.
    column_values_to_select_str = "=? AND ".join([f'"{name}"' for name in table_column_names])

    # Check if such recotd exists in target database
    records = get_specific_record(database, table_name, table_column_names, item_values)
    if not records:
        print(f'WARNING! No such record in database, nothing deleted.')
        return

    # Construct the SQL statement
    cursor.execute(f'DELETE FROM "{table_name}" WHERE {column_values_to_select_str}=?', tuple(item_values))

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    print(f'records: {records} succesfully deleted from database: {database}')
    return records

def delete_many_records(database=str, table_name=str, table_column_names=list, records_values_list=list): # Deletes records from table where records values matches the condition specified.
    # record_values_list must be list of tuples with records for each record to be deleted in matching order as in target sql table. 

    # Connect to database
    conn = sqlite3.connect(database)

    # Create cursor
    cursor = conn.cursor()

    # Create the WHERE clause of the SQL statement to select columns from table in database to compare with criteria provided.
    column_values_to_select_str = "=? AND ".join([f'"{name}"' for name in table_column_names])

    # Check what records will be deleted

    # colums str for select query
    colums_str = ",".join([f'"{name}"' for name in table_column_names])
    print(f'select columns q part: {colums_str}')
    # placeholder tuples for select query
    pt = ", ".join([f'({"?"*len(records_values_list[0])})' for rv in records_values_list])
    print(f'select placeholders q part: {colums_str}')
    # Values list to be passed into Query statement
    print(f'input r v l: {records_values_list}')
    values = [v for r in records_values_list for v in r]
    print(values)

    print(f'final statement:')
    print(f'SELECT rowid, * FROM "{table_name}" WHERE ({colums_str}) IN ({pt}), {values}')

    cursor.execute(f'SELECT rowid, * FROM "{table_name}" WHERE ({colums_str}) IN ({pt})', values)
    records_to_be_deleted = cursor.fetchall()
    
    # If nothing to be deleted → return error info
    if not records_to_be_deleted:
        print(f'WARNING! No record matches given criteria → Nothing deleted.')
        return

    # Construct the SQL statement
    cursor.executemany(f'DELETE FROM "{table_name}" WHERE {column_values_to_select_str}=?', records_values_list)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

    print(f'{len(records_to_be_deleted)} records: {records_to_be_deleted} succesfully deleted from database: {database}')
    return records_to_be_deleted

def find_duplicate_records(database=str, table_name=str):
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Get table columns
    tc = get_table_columns(database, table_name)

    # Table columns STR statement
    str_tc = ", ".join([f'"{c}"' for c in tc])
    # print(str_tc)

    # Try to find all duplicate records in table in given database
    cursor.execute(f'SELECT {str_tc}, COUNT(*) FROM "{table_name}" GROUP BY {str_tc} HAVING COUNT(*) > 1')
    duplicates = cursor.fetchall()
    
    # Close connection
    conn.close()    
    return duplicates

def delete_duplicate_records(database=str, table_name=str): # Function to find duplicate records in given table in given database and delete all but record with lowest rowid.
    print(f'Deleting duplicate records...')
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Get table columns
    tc = get_table_columns(database, table_name)

    # Table columns STR statement
    str_tc = ", ".join([f'"{c}"' for c in tc])
    # print(str_tc)

    # Try to find all duplicate records in table in given database
    cursor.execute(f'SELECT {str_tc}, COUNT(*) FROM "{table_name}" GROUP BY {str_tc} HAVING COUNT(*) > 1')
    duplicates = cursor.fetchall()
    print(duplicates)

    #COnstruct the DELETE statement. This statement wil delete all records from table based on their rowids, where it first makes a group of records with same values for all columns and then deletes all records but one with lowest rowid. 
    # cursor.execute(f'''
    # DELETE FROM "{table_name}" WHERE rowid NOT IN (
    #     SELECT MIN(rowid) FROM "{table_name}" GROUP BY {str_tc})
    # ''')

    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

def create_index_on_column(database=str, table_name=str, column_name=str): # Creates index on column of specific name in specified table in specified database.

    # Connectiong to database
    conn = sqlite3.connect(database)
    
    # Create a cursor
    cursor = conn.cursor()
    print(column_name)
    
    # Naming the index
    c_str = [str.strip() for str in column_name.split(" ")]
    c_str.append("index")
    c_str = "_".join(c_str)
    print(c_str)
    
    # Create index
    cursor.execute(f'CREATE INDEX {c_str}_3 ON {table_name} ("{column_name}")')

    # commiting the changes
    conn.commit()

    # Closing the connection
    conn.close()

def vacuum_database(database=str): # Somehow cleans and rebuilds the database file. Should be used after some major alternation to the database has been made.

    # Connect to the database
    conn = sqlite3.connect(database)
    conn.isolation_level = None

    # Create a cursor
    cursor = conn.cursor()

    # Vacuum the database
    cursor.execute("VACUUM")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_pn_in_monuments(data=list): # Takes list of lines of monument BOM and costructs a list of unique monument: PN pairs. Return list of all unique PNs and their final monumnet.p1:m1, p2:m1, p1:m2, p2:m2 ...

    # list of tuples all pns with its monuments
    all_pn = list()

    for line in data:
        # Set final m and its BOM
        final_monument = line[0]
        monument_bom = line[1:]
        
        for pn in monument_bom:
            if (pn, final_monument) not in all_pn:
                all_pn.append((pn, final_monument))    
    return all_pn