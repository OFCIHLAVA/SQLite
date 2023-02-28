# Module with SQLlite queries

import sqlite3
import os

def check_if_pn_exists(database_path=str, database_name=str, table_name=str, part_numbers=list): # Query to check if there is any record for given part numbers in specified database in specified table.
    
    # Connect to the database
    conn = sqlite3.connect(database_path)

    # Create cursor
    cursor = conn.cursor()

    # Result
    exist = []

    # Check for ech pn from input list
    for pn in part_numbers:

        # Select all records for that part number
        cursor.execute(f'''
        SELECT * FROM "{table_name}"
        WHERE "part number"= "{pn}"
        ''')

        # Fetch the result
        r = cursor.fetchall()

        # Check exists
        if r:
            exist.append((pn, True))
        else:
            exist.append((pn, False))
    
    print(exist)             

    # Close connection
    conn.close()

    # if result empty → pn does not exist in table
    return exist

def query_pn_desc(database_path=str, database_name=str, table_name=str, part_number=str):# Query to get description of searched part number from table "part_numbers" from database "programy"

    import time

    # query start time
    s_time = time.time()

    # Connect to the database
    conn = sqlite3.connect(database_path)

    # Create cursor
    cursor = conn.cursor()

    # Select the description of seatched pn
    cursor.execute(f'SELECT description FROM "{table_name}" WHERE "part number"="{part_number}"')    
    
    # Fetches list of tuples with 0th item = description (desctiption = r[0][0])
    r = cursor.fetchall()
    # print(f'NO record found in table: {table_name} in dataase: {database_name} for PN: {part_number}.') if not r else print(f'Found description {r[0][0]} for pn {part_number}.')

    # Close connection
    conn.close()

    # query end time
    e_time = time.time()

    print(f'result fetched in {round(e_time-s_time, 1)} seconds.')

    return r[0][0] if r else None

def query_pn_in_monuments(database_path=str, database_name=str, table_name=str, part_number=str):# Query to get all the monuments in which PN can be found. Searches in table dilXbouda in database programy.

    import time

    # query start time
    s_time = time.time()

    # Connect to the database
    conn = sqlite3.connect(database_path)

    # Create cursor
    cursor = conn.cursor()

    # Select all the monuments in whoch PN can be found
    cursor.execute(f'SELECT "obsazen v" FROM "{table_name}" WHERE "part number"="{part_number}"')
    
    # Fetches list of tuples with 0th item = description (desctiption = r[0][0])
    r = cursor.fetchall()

    # consolidate result (list of tuples with result monument in 0th index) in list of result monuments
    r = [t[0] for t in r]

    # Close connection
    conn.close()
     
    # print(f'NO record found in table: {table_name} in database: {database_name} for PN: {part_number}.') if not r else print(f'Found description {r[0][0]} for pn {part_number}.')

    # query end time
    e_time = time.time()

    print(f'result fetched in {round(e_time-s_time, 1)} seconds.')

    return r if r else None

def query_pn_monumnets_programs(database_path=str, database_name=str, pn_table=str, pns_monuments=str, monuments_programs=str, part_numbers_list=str): # Query to get all monuments in which PNs from list are used plus theirs monumnets and programs.
    # Returns list of tuples, each containing (searched PN, pn_description, in_monument, monument_desc, monument_program)
    
    import time
    # Start time
    s_time = time.time()

    # Connect to the database
    conn = sqlite3.connect(database_path)

    # cursor
    cursor = conn.cursor()

    # SQL statement to inner join 3 relevant tables and get combined result from them based on searched part_number
    
    # Str placehlolders to replace number of items in input list
    placeholders_str = ", ". join("?"*len(part_numbers_list))
    print(placeholders_str, len(part_numbers_list))
    
    cursor.execute(f'''
    SELECT pns."part number" as pn, pns."description" as desc, dXb."obsazen v", bXp."description", bxp."program", bxp."specific rules"
    FROM "{pn_table}" as pns
    INNER JOIN "{pns_monuments}" as dXb ON pns."part number" = dXb."part number"
    INNER JOIN "{monuments_programs}" as bXp ON dXb."obsazen v" = bXp."final monument"
    WHERE pn IN ({placeholders_str})
    ORDER BY pn, bxp."program"
    ''', part_numbers_list)

    # Fetch result
    r = cursor.fetchall()

    # End time
    e_time = time.time()
    print(f'query fetched in {round(e_time-s_time,2)} seconds ...')
    conn.close()
    
    # insert headings to result
    r.insert(0, ("part number", "description", "in monument","monument description" , "mounment program", "specific monument rules"))    
    
    return r

def query_pn_program(database_path=str, database_name=str, pn_table=str, pns_monuments=str, monuments_programs=str, part_numbers_list=str): # Query to get combination of programs and specific rules for each pn from input list.
    # Returns list of tuples, each containing (searched PN, pn_description, pn_program_combination, pn_specific_rules)
    
    import time
    # Start time
    s_time = time.time()

    # Connect to the database
    conn = sqlite3.connect(database_path)

    # cursor
    cursor = conn.cursor()

    # SQL statement to inner join 3 relevant tables and get combined result from them based on searched part_number
    
    # Str placehlolders to replace number of items in input list
    placeholders_str = ", ". join("?"*len(part_numbers_list))
    print(placeholders_str, len(part_numbers_list))
    
    cursor.execute(f'''
    SELECT pns."part number" as pn, pns."description" as desc,
    GROUP_CONCAT(DISTINCT
    CASE
        WHEN bxp."program" = "NULL" THEN "?"
        ELSE bxp."program"
    END
    )
    as programs,
    GROUP_CONCAT(DISTINCT
    CASE
        WHEN bxp."specific rules" <> "NULL" THEN bxp."specific rules"
        ELSE ""
    END
    ) as s_rules
    FROM "{pn_table}" as pns
    INNER JOIN "{pns_monuments}" as dXb ON pns."part number" = dXb."part number"
    INNER JOIN "{monuments_programs}" as bXp ON dXb."obsazen v" = bXp."final monument"
    WHERE pn IN ({placeholders_str})
    GROUP BY pn
    ''', part_numbers_list)

    # Fetch result
    r = cursor.fetchall()

    # End time
    e_time = time.time()
    
    # Print time taken
    print(f'query fetched in {round(e_time-s_time,2)} seconds ...')

    # Close the connection
    conn.close()
    
    # insert headings to result
    r.insert(0, ("part number", "description", "programs", "specific rules"))    
    
    return r