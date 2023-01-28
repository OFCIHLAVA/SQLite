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
        print(f'Done. Number of records to be inserted into databas: {count_lines}.')
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
    # print(f'Kontrola posleniho pridaneho zaznamu:')
    # print(result)

    # Save the changes
    conn.commit()

    # Close the connection
    conn.close()

def insert_many_records(database=str, table_name=str, records_values=list): # Function to insert multiple new records into the table. Records values is a list of tuples, where order of vaules in tuples must match the table_columns order.
    
    # Get column names of table records are being inserted into
    print(f'getting column names of destination table...')
    table_column_names = get_table_columns(database, table_name)
    print(f'Columns in destination table: {", ".join(table_column_names)}')

    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Insert the new item into the table
        
    # Destinations columns SQL clause str
    columns_str = ", ".join((f'"{t_c}"' for t_c in table_column_names))
    print(columns_str)

    # Values placeholdesr str
    placeholders = ", ".join(["?" for c in table_column_names])
    print(placeholders)

    # Values to be inserted for record (must be is same order as column order)
    # print(item_values)


    # Insert into table
    # cursor.executemany(f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})', records_values)
    for record in records_values:
        try:
            cursor.execute(f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})', record)
        except:
            print(record) 

    print(f'Records succesfully inserted into database:')
    # Check the newly added record
    
    # Last added record rowid
    # last_added_row_id = cursor.lastrowid
    # print(f'posledni pridane id: {last_added_row_id}')

    cursor.execute(f'SELECT rowid, * FROM {table_name}')
    result = cursor.fetchall()
    print(f'Kontrola pridanych zaznamu:')
    #for r in result:
        #print(r)
    print(f'pridano {len(result)} zaznamu.')


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

def update_record(database=str, table_name=str, item_column_name=str, item=str, table_column_names=list, item_values=list): # Updates values of record for existing item ina database - Function to update values of item already found in table, if same item with different values is beeing added to table
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
    # print(set_columns_str+"=?")

    # Add the item variable for the WHERE clause of SQL statement at the end of the list of new values, so that list matches the order of columns being updated.
    # print(f'List of new values without the WHERE item:')
    # print(item_values)
    item_values.append(item)
    # print(f'List of new values with the WHERE item added at the end:')
    # print(item_values)

    cursor.execute(f'UPDATE "{table_name}" SET {set_columns_str}=? WHERE "{item_column_name}"=?', tuple(item_values))
    # Commit the transaction
    conn.commit()

    # Check the updated record
    cursor.execute(f'SELECT rowid, * FROM "{table_name}" WHERE "{item_column_name}"={item}')
    result = cursor.fetchone()
    print(f'Updated record: {result}')

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
    cursor.execute(f'CREATE INDEX {c_str} ON {table_name} ("{column_name}")')

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

def get_pn_in_monuments(data=list): # 

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