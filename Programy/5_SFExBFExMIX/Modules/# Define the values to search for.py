# Define the values to search for
records_values_list = [(1, 2), (30, 300), (100, 999)]

# # Build the query
# query = f'SELECT * FROM "{table_name}" WHERE (column1, column2) IN ({", ".join(["(?, ?)"] * len(records_values_list))})'
# 
# # Execute the query
# cursor.execute(query, [item for sublist in records_values_list for item in sublist])
# 
# # Fetch the results
# records = cursor.fetchall()


l = [item for sublist in records_values_list for item in sublist]
print(l)