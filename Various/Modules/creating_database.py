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
            print(e)
    except Exception as e:
        print(e)
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

def show_all_records_database_in_table(database=str, table_name=str): # Shows all lines in given database and table with its headings.
    
    # Connect to the database
    conn = sqlite3.connect(database)

    # Create a cursor
    cursor = conn.cursor()

    # Retrieve the column names for table
    column_names = get_table_columns(database, table_name)

    # Select all rows from the materials table
    cursor.execute('''
        SELECT rowid, * FROM materials
    ''')
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

def insert_records_into_database_into_table_from_file(database=str, table_name=str, filename=str, uniques_id_column_name=str):  # Funtion to load data from txt. file and insert them
                                                                                                        # into coresponding table in database.
    
    print(f'Inserting records from file {filename} into table {table_name} in database {database}, primary key = {uniques_id_column_name}')

    # Get column names of table records are being inserted into
    print(f'getting column names of destination table...')
    table_column_names = get_table_columns(database, table_name)
    print(f'Columns in destination table: {", ".join(table_column_names)}')

    # Open the text file for reading, specifying the encoding
    print(f'Opening file {filename}...')
    with open(filename, 'r', encoding='utf-8') as f:    
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

        # Creating cursor
        cursor = conn.cursor()

        # Read each subsequent line of the file
        for line in f:
            # Skip blank lines
            if not line.strip():
                continue

            # Skips over headings line to first line of data
            if line == headings_line:
                continue
        
            # Split the line into fields using a tab character as the separator
            fields = line.strip().split('\t')            
            item = fields[unique_item_index]
            print(f'Item to insert: {item}, Values to insert for that item: {fields}.')

            # # Extract the part number and description from the fields
            # part_number = fields[part_number_index]
            # description = fields[description_index]

            # Find the coresponding values from len to insert into table
            # for h in headings_indeces:
            #     print(h)
            item_values = [fields[h[0]] for h in headings_indeces]
            print(f'Values to be insert to table for this item: {item_values}')

            # Check if the item already exists in the table
            print(f'Checking if item {item} already exists in database.')
            if not item_exists(database, table_name, headings[unique_item_index], item):
                print(f'Item {item} no found in table: {table_name} in database {database}.')
                # Insert the item into the table            
                insert_item(database, table_name, table_column_names, item_values)

            else:
                print(f'Item {item} already found in table: {table_name} in database {database}.')
                print(f'Checking, if record for item {item} in table: {table_name} in database {database} is the same as in upload file.')
                if not record_is_same(database, table_name, headings[unique_item_index], item, table_column_names, item_values):
                    print(f'Record is not the same, updating item in database with data from upload file.')  
                    update_record(database, table_name, headings[unique_item_index], item, table_column_names, item_values)
                else:
                    print(f'Record is the same, skipping to next line in upload file.')        

        # Close the connection
        conn.close()            

def insert_item(database=str, table_name=str, table_columns=list, item_values=list): # Function to insert new item into the table. values order must match the table_columns order.
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

    print(f'Record succesfully inserted into database:')
    # Check the newly added record
    
    # Last added record rowid
    last_added_row_id = cursor.lastrowid
    print(f'posledni pridane id: {last_added_row_id}')

    cursor.execute(f'SELECT rowid, * FROM {table_name} WHERE rowid={last_added_row_id}')
    result = cursor.fetchone()
    print(f'Kontrola posleniho pridaneho zaznamu:')
    print(result)

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
    print(item)

    cursor.execute(f'SELECT rowid, * FROM "{table_name}" WHERE "{item_column_name}"="{item}"')
    result = cursor.fetchone()
    print(f'Updated record: {result}')

    # Close the cursor and connection
    cursor.close()
    conn.close()