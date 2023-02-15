import tkinter as tk
from tkinter import ttk, filedialog
import os
import time
from SQL_update.Modules import queries, sqllite
import database_manager
import time



### Setup files

# Nalezeni stavajiciho umisteni
current_folder_path = os.path.dirname(os.path.abspath(__file__))
# Nazev databaze, kam chceme vkladat zaznamy
database_name = 'programy_old.db'
# Sestaveni cesty databaze (predpoklada, ze se databaze nachazi v podslozce SQL_update ve slozce programu.)
database_path = f'{current_folder_path}\\SQL_update\\{database_name}'

# Nazvy tabulek v databazi
pns = "part_numbers"
dXb = "dilyXboudy"
bXp = "boudyXprogramy"

# Root fce

def tab_select(event): # Function to determione, which Tab of window is currently activated and set bindings accordingly
    # Determine which tab currently has focus
    current_tab_index = event.widget.index("current")
    print(current_tab_index, type(current_tab_index))

    # Bind the correct Key shortcuts based on tab being currently selected
    if current_tab_index == 0:
        
        # bind Enter key
        # Run both queries on ENTER pressed
        tab1.bind("<Return>", lambda event: p_run_query_button.invoke())
        entry_box.bind_class("Text", "<Return>", lambda event: p_run_query_button.invoke())

        # bind delete key
        # Clear all text on DEL pressed
        tab1.bind("<Key-Delete>", lambda event: clear_button.invoke())
        entry_box.bind_class("Text", "<Key-Delete>", lambda event: clear_button.invoke())

    elif current_tab_index == 1:
        
        # bind Enter key
        # Search for the part number and monument
        tab2.bind("<Return>", lambda event: tab2_pn_search_button.invoke())
        tab2_t_pn.bind_class("Text", "<Return>", lambda event: tab2_pn_search_button.invoke())
        
        # bind delete key
        # Clear the search windows
        tab2.bind("<Key-Delete>", lambda event: tab2_clear_search_button.invoke())
        tab2_t_pn.bind_class("Text", "<Key-Delete>", lambda event: tab2_clear_search_button.invoke())

    elif current_tab_index == 2:
        
        # bind Enter key
        # Search for the part number and monument
        tab3.bind("<Return>", lambda event: tab3_pn_search_button.invoke())
        tab3_t_m.bind_class("Text", "<Return>", lambda event: tab3_pn_search_button.invoke())
        
        # bind delete key
        # Clear the search windows
        tab3.bind("<Key-Delete>", lambda event: tab2_clear_search_button.invoke())
        tab2_t_pn.bind_class("Text", "<Key-Delete>", lambda event: tab3_clear_search_button.invoke())

def key_bindings_by_tabs(current_tab=str):
    pass

# TAB1 fce
def run_get_programy(): # Function to take input from user and run get program query on it to get program of pns inputed. KEY PRESSED VERSION
    
    # First clear programy ouput widget
    clear_programy_output()

    # Get user input from entry text box.
    user_input = list(set([pn.strip() for pn in entry_box.get(1.0, tk.END).split("\n") if pn != ""]))
    print(f'mam input')
    # If input not empty → update the output text box with the query result
    if len(user_input) != 0:

        # Check the input list for parts not in database
        check_pns_in_database = queries.check_if_pn_exists(database_path, database_name, pns, user_input)
        pns_not_in_database = [r[0] for r in check_pns_in_database if not r[1]]
        print(f'PNs not in database: {pns_not_in_database}')
        
        # Run your query using the input part numbers list (result is list of tuples with results, with headings on first position of list)
        print(f'hledam programy')
        pgms_result = queries.query_pn_program(database_path, database_name, pns, dXb, bXp, user_input)
        pr = pgms_result
        print(f'Mam to - jdu tisknout')
        # For each result line, put that line into output text window + input new line character        
        # enable inserting into output window
        p_output_box['state'] = 'normal'
        
        # Determine the maximum length of strings in each column / error message when pn not found

        str_pn_not_in_database = "P/N not in database"
        spnid = str_pn_not_in_database

        col0_width = max(max(len(t[0]) for t in pr), len(spnid))+4
        col1_width = max(max(len(t[1]) for t in pr), len(spnid))+4
        col2_width = max(max(len(t[2]) for t in pr), len(spnid))+4
        col3_width = max(max(len(t[3]) for t in pr), len(spnid))+4

        # Transform list of tuples into list of lists
        pr_list = [[value for value in tup] for tup in pr]

        # Print the result with equal column widths
        for line in pr_list:
            # Remove "," from rules column if it is on 1st position? Null value for rules in database
            if line[3]:
                if line[3][0] == ",":
                    line[3] = line[3][1:]
            # Create formated string to insert in output box
            f_line = "{:<{}}\t{:<{}}\t{:<{}}\t{:<{}}".format(line[0], col0_width, line[1], col1_width, line[2], col2_width, line[3], col3_width)

            # Insert string into output
            p_output_box.insert(tk.END, f_line)
            p_output_box.insert(tk.END, "\n")

        # Also check input list for part numbers not in database
        for pn in pns_not_in_database:
            # Create formated string to insert in output box
            f_line = "{:<{}}\t{:<{}}\t{:<{}}\t{:<{}}".format(pn, col0_width, spnid, col1_width, spnid, col2_width, spnid, col3_width)

            # Insert string into output
            p_output_box.insert(tk.END, f_line)
            p_output_box.insert(tk.END, "\n")

        # Formating the output text to be multicolored

        p_output_box.tag_config("lightblue", background="lightblue")
        p_output_box.tag_config("lightgray", background="lightgray")

        for i in range(2, int(p_output_box.index("end").split(".")[0]), 2):
            p_output_box.tag_add("lightblue", f"{i}.0", f"{i}.end")

        for i in range(3, int(p_output_box.index("end").split(".")[0]), 2):
            p_output_box.tag_add("lightgray", f"{i}.0", f"{i}.end")

        # after done, disable inserting into output window
        p_output_box['state'] = 'disabled'

def run_get_monumenty(): # Function to take input from user and run get monuments query on it to get monumnets in which pns inputed are located.
    
    # First clear boudy ouput widget
    clear_boudy_output()

    # Get user input from entry text box.
    user_input = list(set([pn.strip() for pn in entry_box.get(1.0, tk.END).split("\n") if pn != ""]))
    
    # If input not empty → update the output text box with the query result
    if len(user_input) != 0:

        # Check the input list for parts not in database
        check_pns_in_database = queries.check_if_pn_exists(database_path, database_name, pns, user_input)
        pns_not_in_database = [r[0] for r in check_pns_in_database if not r[1]]
        print(f'PNs not in database: {pns_not_in_database}')

        # Run your query using the input part numbers list (result is list of tuples with results, with headings on first position of list)
        monuments_result = queries.query_pn_monumnets_programs(database_path, database_name, pns, dXb, bXp, user_input)
        mr = monuments_result

        # For each result line, put that line into output text window + input new line character        
        # enable inserting into output window
        b_output_box['state'] = 'normal'
        
        # Determine the maximum length of strings in each column / error message when pn not found

        str_pn_not_in_database = "P/N not in database"
        spnid = str_pn_not_in_database

        col0_width = max(max(len(t[0]) for t in mr), len(spnid))+4
        col1_width = max(max(len(t[1]) for t in mr), len(spnid))+4
        col2_width = max(max(len(t[2]) for t in mr), len(spnid))+4
        col3_width = max(max(len(t[3]) for t in mr), len(spnid))+4
        col4_width = max(max(len(t[4]) for t in mr), len(spnid))+4
        col5_width = max(max(len(t[5]) for t in mr), len(spnid))+4

        # Transform list of tuples into list of lists
        mr_list = [[value for value in tup] for tup in mr]

        # Print the result with equal column widths   
        
        for line in mr_list:
            # Remove "," from rules column if it is on 1st position? Null value for rules in database
            if line[5]:
                if line[5][0] == ",":
                    line[5] = line[5][1:]
            # Create formated string to insert in output box
            f_line = "{:<{}}\t{:<{}}\t{:<{}}\t{:<{}}\t{:<{}}\t{:<{}}".format(line[0], col0_width, line[1], col1_width, line[2], col2_width, line[3], col3_width, line[4], col4_width, line[5], col5_width)

            # Insert string into output
            b_output_box.insert(tk.END, f_line)
            b_output_box.insert(tk.END, "\n")

        # Also show info for Part numbers not found in databas

        str_not_found = "P/N not in database"
        snf = str_not_found

        for pn in pns_not_in_database:
            # Create formated string to insert in output box
            f_line = "{:<{}}\t{:<{}}\t{:<{}}\t{:<{}}\t{:<{}}\t{:<{}}".format(pn, col0_width, spnid, col1_width, spnid, col2_width, spnid, col3_width, spnid, col4_width, spnid, col5_width)

            # Insert string into output
            b_output_box.insert(tk.END, f_line)
            b_output_box.insert(tk.END, "\n")        
        
        # Formating the output text to be multicolored

        b_output_box.tag_config("lightgreen", background="lightgreen")
        b_output_box.tag_config("lightgray", background="lightgray")

        for i in range(2, int(b_output_box.index("end").split(".")[0]), 2):
            b_output_box.tag_add("lightgreen", f"{i}.0", f"{i}.end")

        for i in range(3, int(b_output_box.index("end").split(".")[0]), 2):
            b_output_box.tag_add("lightgray", f"{i}.0", f"{i}.end")

        # after done, disable inserting into output window
        b_output_box['state'] = 'disabled'
        
        # after done, disable inserting into output window
        b_output_box['state'] = 'disabled'

def run_queries(): # Function to run both queries above together
    run_get_programy()
    run_get_monumenty()

def key_run_queries(event): # Function to bind to ENTER key to run both queries above together. Event in mandatory paramater representing the key pressed in this case.
    run_get_programy()
    run_get_monumenty()

def clear_everything(): # Function to clear all entry and output windows.
    # Clear entry window
    entry_box.delete(1.0, tk.END)
    # Clear the output windows
    clear_all_outputs()

def key_clear_everything(event):  # Event in mandatory paramater representing the key pressed in this case.
    clear_everything()

def clear_all_outputs(): # Function to clear all output windows.
    # Clear programs output window
    clear_programy_output()
    # Clear boudy output window
    clear_boudy_output() 

def clear_programy_output(): # Function to clear programs output windows.
    # Clear programs output window
    p_output_box['state'] = 'normal'
    p_output_box.delete(1.0, tk.END)
    p_output_box['state'] = 'disabled'

def clear_boudy_output(): # Function to clear boudy output windows.
    # Clear boudy output window
    b_output_box['state'] = 'normal'
    b_output_box.delete(1.0, tk.END)
    b_output_box['state'] = 'disabled'    

def copy_programy_output():
    x = p_output_box.get(1.0, tk.END)
    p_output_box.clipboard_clear()
    p_output_box.clipboard_append(x)

def copy_boudy_output():
    y = b_output_box.get(1.0, tk.END)
    b_output_box.clipboard_clear()
    b_output_box.clipboard_append(y)

def tab1_enter_key_press(event): # Function to bind the Enter key to the button query button
    run_queries()

# TAB 2 fce
def select_cq_file():
    
    file_path = filedialog.askopenfilename(title="Select CQ report txt file", filetypes=(("Text files", "*.txt"),))
    print(file_path)
    # Insert string into output
    tab2_cq_file_path_box['state'] = 'normal'
    tab2_cq_file_path_box.delete(1.0, tk.END)
    tab2_cq_file_path_box.insert(1.0, file_path, "center")
    tab2_cq_file_path_box['state'] = 'disabled'
    tab2_cq_file_path_box.tag_configure("center", justify="center")

def select_txt_file():
    
    file_path = filedialog.askopenfilename(title="Select txt file", filetypes=(("Text files", "*.txt"),))
    print(file_path)
    # Insert string into output
    tab2_txt_file_path_box['state'] = 'normal'
    tab2_txt_file_path_box.delete(1.0, tk.END)
    tab2_txt_file_path_box.insert(1.0, file_path, "center")
    tab2_txt_file_path_box['state'] = 'disabled'
    tab2_txt_file_path_box.tag_configure("center", justify="center")

def process_cq_file(database_path=str, cq_filepath=str): # Function to process cq txt file and add its contents into databased
    # helper function to close prompt window
    def close_cq_update_message():
        new_window.destroy()

    # CLean input path
    cq_filepath = cq_filepath.strip().replace("\n", "")

    # Create a new window to block other actions while updating database
    new_window = tk.Toplevel(root)
    new_window.title("BOM update status")
    new_window.iconbitmap(f'{current_folder_path}\\graphics\\into db icon.ico')
    new_window.geometry("450x200")
    new_window.resizable(False, False)

    # Create txt widget to display result text of the update
    txt = tk.Text(new_window, height=5, width=50 ,font=("Verdana", 10), padx=10, pady=10)
    txt.pack()
    start_text = f'Vkladam data do databaze, this may take a while...\nDO NOT CLOSE THE PROGRAM!\n\n'
    txt.tag_configure("center", justify="center")
    txt.insert(tk.END, start_text, "center")
    txt['state'] = "disabled"
    time.sleep(1)
    
    # This blocks the other windows
    new_window.grab_set()   
    
    # Updating function produces result message to be displayed
    txt['state'] = "normal"
    txt.delete(1.0, tk.END)
    output_text = database_manager.update_database_bom_from_cq_file(database_path, cq_filepath)
    txt.insert(tk.END, output_text, "center")
    txt['state'] = "disabled"

    # Show button to close window
    tab2_button_exit = tk.Button(new_window, width=14, text = "OK", font=("Verdana", 16, "bold"), padx=20, pady=20, command=close_cq_update_message)
    tab2_button_exit.pack()

    # Finaly clears the cq select file path window
    tab2_cq_file_path_box['state'] = 'normal'
    tab2_cq_file_path_box.delete(1.0, tk.END)
    tab2_cq_file_path_box['state'] = 'disabled'

def bom_process_txt_file(database_path=str, txt_filepath=str): # Function to process txt file and add its contents into database
        
    # helper function to close prompt window
    def close_txt_update_message():
        new_window.destroy()

    # CLean input path
    txt_filepath = txt_filepath.strip().replace("\n", "")

    # Create a new window to block other actions while updating database
    new_window = tk.Toplevel(root)
    new_window.title("txt file update status")
    new_window.iconbitmap(f'{current_folder_path}\\graphics\\into db icon.ico')
    new_window.geometry("450x200")
    new_window.resizable(False, False)

    # Create txt widget to display result text of the update
    txt = tk.Text(new_window, height=5, width=50 ,font=("Verdana", 10), padx=10, pady=10)
    txt.pack()
    start_text = f'Vkladam data do databaze, this may take a while...\nDO NOT CLOSE THE PROGRAM!\n\n'
    txt.tag_configure("center", justify="center")
    txt.insert(tk.END, start_text, "center")
    txt['state'] = "disabled"
    time.sleep(1)
    
    # This blocks the other windows
    new_window.grab_set()   
    
    # Updating function produces result message to be displayed
    txt['state'] = "normal"
    txt.delete(1.0, tk.END)
    output_text = database_manager.update_database_bom_from_txt_list(database_path, txt_filepath)
    txt.insert(tk.END, output_text, "center")
    txt['state'] = "disabled"

    # Show button to close window
    tab2_button_exit = tk.Button(new_window, width=14, text = "OK", font=("Verdana", 16, "bold"), padx=20, pady=20, command=close_txt_update_message)
    tab2_button_exit.pack()

    # Finaly clears the txt select file path window
    tab2_txt_file_path_box['state'] = 'normal'
    tab2_txt_file_path_box.delete(1.0, tk.END)
    tab2_txt_file_path_box['state'] = 'disabled'

def add_pn_monument(database_path=str, pn=str, monument=str): # Function to insert given pn and monument as pair into BOM database

    # Clean inputs
    pn=pn.replace(" ","").replace("\n", "").replace("\t", "")
    monument=monument.replace(" ","").replace("\n", "").replace("\t", "")

    # Insert record only if something in both search windows
    if pn and monument:
        # ADD record into BOM table in database based on pn and monumet given through search txts.
        added_record = sqllite.insert_record(database_path, dXb, ["part number", "obsazen v"], [pn, monument])
        print(added_record)
        
        # If record inserted succesfully, add the monument from record also into database monuments with ? as default values, if such record not already in database.
        if added_record:            
            # Check if such record alreay in database
            already_in_db = sqllite.get_specific_record(database_path, 'boudyXprogramy', ["final monument"], [monument])
            pass            
            if not already_in_db:
                # If not → add monument
                print(f'This monument not yet in database → inserting: {monument} with default values "?"')
                inserted_monument = sqllite.insert_record(database_path, 'boudyXprogramy', ["final monument", "description", "program", "specific rules"], [monument, "?", "?", "?"])
                print(inserted_monument)

        # Show info wheter something was added
        if added_record:
            message = f'record: {added_record}\nADDED into BOM database!'
            print(message)
            # Add Label Saying this record has been Added to database
            tab2_l_message.config(font=("Verdana", 11, "bold"), background="dark green", foreground="white",text=message)
        else:
            message = f'Warning! Nothing added, check why.'
            tab2_l_message.config(font=("Verdana", 11, "bold"), background="yellow", foreground="black",text=message)
        # hide the action button
        tab2_button_action_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

def search_pn_in_monument(database_path=str, pn=str, monument=str): # Function to find if given part number in given monument has already record in database. Returns record, if found else None.
    
    # Clean inputs
    pn=pn.replace(" ","").replace("\n", "").replace("\t", "")
    monument=monument.replace(" ","").replace("\n", "").replace("\t", "")
    
    # Search only if something in both search windows
    if pn and monument:
    # Get specific record
        record = database_manager.find_pn_in_monument(database_path, pn, monument)
        print(record)

        # Display info, wheter such record already in database or not

        # If record already in database → show info and create option to delete record from database
        if record:
            # Change Label to Saying this record already in database
            tab2_l_message.config(font=("Verdana", 11, "bold"), background="green", foreground="white" ,text="Such record already exists!")
            # Change Action button to Delete record action
            tab2_button_action_record.config(width=6, font=("Verdana", 9, "bold"), background="red", foreground="white" ,text="DELETE\nrecord",padx=3 , command=lambda:delete_pn_monument(database_path, tab2_t_pn.get(1.0, tk.END), tab2_t_im.get(1.0, tk.END)))
            
            ## Add button to delete record 
            #button_del_record = tk.Button(tab2, width=6, font=("Verdana", 9, "bold"), background="red", foreground="white" ,text="DELETE\nrecord", command=lambda:delete_pn_monument(database_path, t_pn.get(1.0, tk.END), t_im.get(1.0, tk.END)))
            #button_del_record.grid(row=3, column=2, columnspan=1, pady=2 , padx=0, sticky="nse")

        # else → show info and create option to add that record into database
        else:
            # Add Label Saying this record already in database
            tab2_l_message.config(font=("Verdana", 11, "bold"), background="red", foreground="white" ,text="No such record in BOM database!")
            # Change Action button to ADD record action
            tab2_button_action_record.config(width=6, font=("Verdana", 9, "bold"), background="green", foreground="white" ,text="ADD\nrecord",padx=3, command=lambda:add_pn_monument(database_path, tab2_t_pn.get(1.0, tk.END), tab2_t_im.get(1.0, tk.END)))

            # # Add button to add record 
            # button_add_record = tk.Button(tab2, width=6, font=("Verdana", 9, "bold"), background="green", foreground="white" ,text="ADD\nrecord", command=lambda:add_pn_monument(database_path, t_pn.get(1.0, tk.END), t_im.get(1.0, tk.END)))
            # button_add_record.grid(row=3, column=2, columnspan=1, pady=2 , padx=0, sticky="nse")

def delete_pn_monument(database_path=str, pn=str, monument=str): # Function to delete specific record from database
    
    # Clean inputs
    pn=pn.replace(" ","").replace("\n", "").replace("\t", "")
    monument=monument.replace(" ","").replace("\n", "").replace("\t", "")

    # Delete only if something in both search windows
    if pn and monument:
        # Delete record from BOM table in database based on pn and monumet given through search txts.
        deleted_record = sqllite.delete_record(database_path, dXb, ["part number", "obsazen v"], [pn, monument])

        # Show info wheter something was deleted
        if deleted_record:
            message = f'record: {deleted_record}\nDELETED from BOM database!'
        else:
            message = f'Warning! No such record in database. Nothing deleted.'    
        # Add Label Saying this record has been deleted from database
        tab2_l_message.config(font=("Verdana", 11, "bold"), background="orange", foreground="black" ,text=message)

        # hide the action button
        tab2_button_action_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

def clear_pn_in_monument_search():
    # Clear the PN search window
    tab2_t_pn.delete(1.0, tk.END)

    # Clear tin monument search window
    tab2_t_im.delete(1.0, tk.END)

    # Clear the message label
    tab2_l_message.config(font=("Verdana", 11, "bold"),  background=root['bg'], text="")

    # hide the action button
    tab2_button_action_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

def pass_function():
    pass

def tab2_enter_key_press(event): # Function to bind the Enter key to the button query button
    search_pn_in_monument(database_path, tab2_t_pn.get(1.0, tk.END), tab2_t_im.get(1.0, tk.END))

# TAB 3 fce
def search_for_monument(database_path=str, monument=str): # .Function to search for specific monumnet and its parameters. Actiovates action buttons accordingly.
    
    # Clean inputs
    monument=monument.replace(" ","").replace("\n", "").replace("\t", "")
    
    # Search only if something in monument search windows
    if monument:
        # Clear search windows before new search

        # Clear description
        tab3_t_d['state'] = 'normal'
        tab3_t_d.delete(1.0, tk.END)
        tab3_t_d['state'] = 'disabled'
    
        # Clear Program window
        tab3_t_p['state'] = 'normal'
        tab3_t_p.delete(1.0, tk.END)
        tab3_t_p['state'] = 'disabled'
    
        # Clear specific rules window
        tab3_t_sr['state'] = 'normal'
        tab3_t_sr.delete(1.0, tk.END)
        tab3_t_sr['state'] = 'disabled'
        
        # Get specific record
        record = sqllite.get_specific_record(database_path, 'boudyXprogramy', ["final monument"], [monument])
        print(record)

        # Display info, wheter such record already in database or not

        # If record already in database → show monument info and create option to delete / update record
        if record:
            # queru returns list of tuples
            record = record[0]

            # Get data for given monument
            description = record[2] if record[2] != 'NULL' else '?'
            program = record[3] if record[3] != 'NULL' else '?'
            spec_rules = record[4] if record[4] != 'NULL' else '?'

            # Insert data into txt windows
            tab3_t_d['state'] = 'normal'
            tab3_t_d.insert(tk.END, description)
            tab3_t_d['state'] = 'disabled'

            tab3_t_p['state'] = 'normal'
            tab3_t_p.insert(tk.END, program)
            tab3_t_p['state'] = 'disabled'
            
            tab3_t_sr['state'] = 'normal'
            tab3_t_sr.insert(tk.END, spec_rules)
            tab3_t_sr['state'] = 'disabled'
            
            # Change Label to Saying this record already in database
            tab3_l_message.config(font=("Verdana", 11, "bold"), background="green", foreground="white" ,text="Such Monument already exists in database!")
            
            # Change Action button to Delete record action
            tab3_button_action_record.config(width=6, font=("Verdana", 9, "bold"), background="red", foreground="white" ,text="DELETE\nrecord",padx=3 , command=confirm_deletion)
            
            # Change update button to Allow update of record action
            tab3_button_update_record.config(width=6, font=("Verdana", 9, "bold"), background="orange", foreground="black" ,text="UPDATE\nrecord",padx=3 , command=update_monument)

        # else → show info and create option to add that record into database
        else:
            # Add Label Saying this record already in database
            tab3_l_message.config(font=("Verdana", 11, "bold"), background="red", foreground="white" ,text="NO record for this monument in database!")
            
            # Change update button to create record action
            tab3_button_update_record.config(width=6, font=("Verdana", 9, "bold"), background="orange", foreground="white" ,text="CREATE\nrecord",padx=3, command=create_monument_record)
            
            # Hide ADD button
            tab3_button_action_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

def create_monument_record():
    # Clean inputs
    monument = tab3_t_m.get(1.0,tk.END)
    monument = monument.replace(" ","").replace("\n", "").replace("\t", "")

    if monument:
        ## Enable adding / editing record data
        # enable description
        tab3_t_d['state'] = 'normal'
        tab3_t_d.config(background="white", foreground="black")

        # enable  Program window
        tab3_t_p['state'] = 'normal'
        tab3_t_p.config(background="white", foreground="black")

        # enable  specific rules window
        tab3_t_sr['state'] = 'normal'
        tab3_t_sr.config(background="white", foreground="black")

        ## Show message for user, to create record for given monument        
        # Change Label to Saying how to create record
        tab3_l_message.config(font=("Verdana", 11, "bold"), background="orange", foreground="black" ,text="↑ Insert description, program and specific rules\nfor given monument, then click ADD record button. ↑")

        # hide the create (update) button
        tab3_button_update_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

        # Change action button to show ADD recor
        tab3_button_action_record.config(width=6, font=("Verdana", 9, "bold"), background="green", foreground="white" ,text="ADD\nrecord",padx=3 , command=lambda:add_monument_record(database_path, tab3_t_m.get(1.0,tk.END),tab3_t_d.get(1.0,tk.END),tab3_t_p.get(1.0,tk.END), tab3_t_sr.get(1.0,tk.END)))

def add_monument_record(database_path=str, monument=str, description=str, program=str, spec_rules=str): # Function to take user input for given monument and create such record in database. 
    
    # Clean inputs
    monument = monument.replace(" ","").replace("\n", "").replace("\t", "")
    description = description.strip().replace("\n", "").replace("\t", "")
    program = program.replace(" ","").replace("\n", "").replace("\t", "")
    spec_rules = spec_rules.strip().replace("\n", "").replace("\t", "")

    # Only insert record, if something in monument search window
    if monument:
        # Add monument
        inserted_monument = sqllite.insert_record(database_path, 'boudyXprogramy', ["final monument", "description", "program", "specific rules"], [monument, description, program, spec_rules])

        # Show info wheter something was added
        if inserted_monument:
            message = f'record: {inserted_monument}\nADDED into database!'
            print(message)
            # Add Label Saying this record has been Added to database
            tab3_l_message.config(font=("Verdana", 11, "bold"), background="dark green", foreground="white",text=message)
        else:
            message = f'Warning! Nothing added, check why.'
            tab3_l_message.config(font=("Verdana", 11, "bold"), background="yellow", foreground="black",text=message)
        # hide the action button
        tab3_button_action_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

        # Finaly disable the search windows
        # disable description and set bacj default formating
        tab3_t_d.config(background="gray", foreground="white")
        tab3_t_d['state'] = 'disabled'
        
        # disable Program window
        tab3_t_p.config(background="gray", foreground="white") 
        tab3_t_p['state'] = 'disabled' 
        
        # disable specific rules window
        tab3_t_sr.config(background="gray", foreground="white") 
        tab3_t_sr['state'] = 'disabled'      

def clear_monument_search():
    # Clear the Monument search window
    tab3_t_m['state'] = 'normal'
    tab3_t_m.delete(1.0, tk.END)

    # Clear description
    tab3_t_d['state'] = 'normal'
    tab3_t_d.delete(1.0, tk.END)
    tab3_t_d['state'] = 'disabled'

    # Clear Program window
    tab3_t_p['state'] = 'normal'
    tab3_t_p.delete(1.0, tk.END)
    tab3_t_p['state'] = 'disabled'

    # Clear specific rules window
    tab3_t_sr['state'] = 'normal'
    tab3_t_sr.delete(1.0, tk.END)
    tab3_t_sr['state'] = 'disabled'

    # Clear the message label
    tab3_l_message.config(font=("Verdana", 11, "bold"),  background=root['bg'], text="")

    # hide the action button
    tab3_button_action_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)
    
    # hide the update button
    tab3_button_update_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

def update_monument(): # Function to change data of current record 

    # Clean input
    monument = tab3_t_m.get(1.0,tk.END)
    monument = monument.replace(" ","").replace("\n", "").replace("\t", "")

    # Only let update, if something in monuments input window
    if monument:
        # Disable the monument window to prevent unwanted change of monument being updated
        tab3_t_m['state'] = 'disabled'

        # Enable editing other monument info
        # enable description
        tab3_t_d['state'] = 'normal'
        tab3_t_d.config(background="white", foreground="black")
    
        # enableProgram window
        tab3_t_p['state'] = 'normal'
        tab3_t_p.config(background="white", foreground="black")
    
        # enable specific rules window
        tab3_t_sr['state'] = 'normal'
        tab3_t_sr.config(background="white", foreground="black")

        # Change message Label to Saying how to update record
        tab3_l_message.config(font=("Verdana", 11, "bold"), background="orange", foreground="black" ,text="↑ EDIT description, program and specific rules\nfor given monument, then click SAVE changes button to commit changes. ↑")

        # hide the create (update) button
        tab3_button_update_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

        # Change action button to show COMMIT changes for record
        tab3_button_action_record.config(width=6, font=("Verdana", 9, "bold"), background="green", foreground="white" ,text="SAVE\nchanges",padx=3 , command=save_updated_monument)        

def save_updated_monument(): # Function to actually save the changes to database (part of update record)
    
    # Get inputs
    monument = tab3_t_m.get(1.0,tk.END)
    description = tab3_t_d.get(1.0,tk.END)
    program = tab3_t_p.get(1.0,tk.END)
    spec_rules = tab3_t_sr.get(1.0,tk.END)    
    
    # Clean inputs
    monument = monument.replace(" ","").replace("\n", "").replace("\t", "")
    description = description.strip().replace("\n", "").replace("\t", "")
    program = program.replace(" ","").replace("\n", "").replace("\t", "")
    spec_rules = spec_rules.strip().replace("\n", "").replace("\t", "")

    # Only update, if there is some monument to update
    if monument:
        # Actual update query
        updated_monument = sqllite.update_record(database_path, 'boudyXprogramy', "final monument", monument, ["final monument", "description", "program", "specific rules"], [monument, description, program, spec_rules])
        # Show info wheter something was updated
        if updated_monument:
            message = f'Monument: {monument} updated in database to:\n{updated_monument}'
            print(message)
            # Add Label Saying this record has been updated to database
            tab3_l_message.config(font=("Verdana", 11, "bold"), background="dark green", foreground="white",text=message)
        else:
            message = f'Warning! Nothing updated, check why.'
            tab3_l_message.config(font=("Verdana", 11, "bold"), background="yellow", foreground="black",text=message)
        
        # hide the action button
        tab3_button_action_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)
        
        # Finaly disable the search windows
        # disable description
        tab3_t_d['state'] = 'disabled'
        tab3_t_d.config(background="gray", foreground="white")
    
        # disable Program window
        tab3_t_p['state'] = 'disabled'
        tab3_t_p.config(background="gray", foreground="white")
    
        # disable specific rules window
        tab3_t_sr['state'] = 'disabled'
        tab3_t_sr.config(background="gray", foreground="white")

def delete_monument(): # Function to delete records for given monument from database
    
    # Clean input
    monument = tab3_t_m.get(1.0,tk.END)
    monument = monument.replace(" ","").replace("\n", "").replace("\t", "")

    # Only delete, if something in monuments input window
    if monument:
        # Delete given monument from database
        deleted_monuments = sqllite.delete_record(database_path, 'boudyXprogramy', ["final monument"], [monument])
        # Show info wheter something was deleted
        if deleted_monuments:
            message = f'Monument: {monument} deleted from database:\n{deleted_monuments}'
            print(message)
            # Add Label Saying this record has been deleted from database
            tab3_l_message.config(font=("Verdana", 11, "bold"), background="red", foreground="black",text=message)
        else:
            message = f'Warning! Nothing deleted, check why.'
            tab3_l_message.config(font=("Verdana", 11, "bold"), background="yellow", foreground="black",text=message)        

        # hide the action button
        tab3_button_action_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)

        # Finaly Clear search windows

        # Clear description
        tab3_t_d['state'] = 'normal'
        tab3_t_d.delete(1.0, tk.END)
        tab3_t_d['state'] = 'disabled'
    
        # Clear Program window
        tab3_t_p['state'] = 'normal'
        tab3_t_p.delete(1.0, tk.END)
        tab3_t_p['state'] = 'disabled'
    
        # Clear specific rules window
        tab3_t_sr['state'] = 'normal'
        tab3_t_sr.delete(1.0, tk.END)
        tab3_t_sr['state'] = 'disabled'

def confirm_deletion(): # Helper function to confirm deletion       
    
    # Clean input
    monument = tab3_t_m.get(1.0,tk.END)
    monument = monument.replace(" ","").replace("\n", "").replace("\t", "")

    # Only delete, if something in monuments input window
    if monument:    
        # disable monument search window to prevent unwanted changes
        tab3_t_m['state'] = 'disabled'
        
        message = f'Do you really want to delete monument: {monument} from database?\nThis cannot be undone! Please confirm deletion →'
        # show message if really want to delete monument
        tab3_l_message.config(font=("Verdana", 11, "bold"), background="yellow", foreground="black",text=message)
        
        # hide the create (update) button
        tab3_button_update_record.config(width=6, relief="sunken", background=root['bg'], text="", bd=0,command=pass_function)
        
        # Change Action button to Confirm Delete record action
        tab3_button_action_record.config(width=8, font=("Verdana", 9, "bold"), background="red", foreground="white" ,text="CONFRIM\ndeletion",padx=3 , command=delete_monument)

def monuments_process_txt_file(database_path=str, txt_filepath=str): # Function to process txt file and add its contents into database
    # helper function to close prompt window
    def close_txt_update_message():
        new_window.destroy()

    # CLean input path
    txt_filepath = txt_filepath.strip().replace("\n", "")

    # Create a new window to block other actions while updating database
    new_window = tk.Toplevel(root)
    new_window.title("txt file update status")
    new_window.iconbitmap(f'{current_folder_path}\\graphics\\into db icon.ico')
    new_window.geometry("450x200")
    new_window.resizable(False, False)

    # Create txt widget to display result text of the update
    txt = tk.Text(new_window, height=5, width=50 ,font=("Verdana", 10), padx=10, pady=10)
    txt.pack()
    start_text = f'Vkladam data do databaze, this may take a while...\nDO NOT CLOSE THE PROGRAM!\n\n'
    txt.tag_configure("center", justify="center")
    txt.insert(tk.END, start_text, "center")
    txt['state'] = "disabled"
    time.sleep(1)
    
    # This blocks the other windows
    new_window.grab_set()   
    
    # Updating function produces result message to be displayed
    txt['state'] = "normal"
    txt.delete(1.0, tk.END)
    output_text = database_manager.add_many_monumnets(database_path, txt_filepath)
    txt.insert(tk.END, output_text, "center")
    txt['state'] = "disabled"

    # Show button to close window
    tab3_button_exit = tk.Button(new_window, width=14, text = "OK", font=("Verdana", 16, "bold"), padx=20, pady=20, command=close_txt_update_message)
    tab3_button_exit.pack()

    # Finaly clears the txt select file path window
    tab3_txt_file_path_box['state'] = 'normal'
    tab3_txt_file_path_box.delete(1.0, tk.END)
    tab3_txt_file_path_box['state'] = 'disabled'

def tab3_select_txt_file():
    
    file_path = filedialog.askopenfilename(title="Select txt file", filetypes=(("Text files", "*.txt"),))
    print(file_path)
    # Insert string into output
    tab3_txt_file_path_box['state'] = 'normal'
    tab3_txt_file_path_box.delete(1.0, tk.END)
    tab3_txt_file_path_box.insert(1.0, file_path, "center")
    tab3_txt_file_path_box['state'] = 'disabled'
    tab3_txt_file_path_box.tag_configure("center", justify="center")


### CREATE THE MAIN WINDOW
root = tk.Tk()
root.minsize(width=500, height=720)
# root.maxsize(width=600, height=400)

root.title("Ukazovadlo programů SFE x BFE x MIX Verze 2.0")
root.iconbitmap("Y:\\Departments\\Sales and Marketing\\Aftersales\\11_PLANNING\\23_Python_utilities\\5_SFExBFExMIX\\graphics\\icon4.ico")
root.geometry('900x600+0+3')

# FONT
font = ("Verdana", 12, "bold")
font2 = ("Verdana", 10)
font3 = ("Verdana", 8)
font4 = ("Verdana", 12)

# Create notebook (multitab window)
notebook = ttk.Notebook(root)

##### Create 1st tab
tab1 = ttk.Frame(notebook)
# This makes collumns in tab to expand and fill available sapce when window is resized
tab1.columnconfigure(0, minsize=100, weight=1)
tab1.columnconfigure(1, minsize=100, weight=10)
# This makes rows in tab to expand and fill available sapce when window is resized
tab1.rowconfigure(2, minsize=100, weight=1)
tab1.rowconfigure(6, minsize=200, weight=10)


# Create a label for the part number input
part_number_label = tk.Label(tab1, text="↓ Enter part numbers ↓", font=font, background="gray", foreground="white", borderwidth=0, relief="solid")
part_number_label.grid(row=0, rowspan=2, column=0, sticky="news")

# Create a button to copy the programs query output
p_copy_output_button = tk.Button(tab1, text="↓ COPY result programs ↓", command=copy_programy_output, font=("Verdana", 11, "bold"), background="gray", foreground="white")
p_copy_output_button.grid(row=0, column=1, sticky="nsew")

# Create a entry box for the part number input
entry_box = tk.Text(tab1, wrap="none", borderwidth=1, width=15, height=10, font=("Verdana", 10, "bold"), background="dark gray", foreground="white", relief="solid")
entry_box.grid(row=2, column=0, sticky="nsew")

# Create an output box for the programs query result
# p_output_box = tk.Text(root,width=130, borderwidth=3)
p_output_box = tk.Text(tab1, wrap="none", borderwidth=1, height=1, background="dark gray", foreground="black", relief="solid")
p_output_box['state'] = 'disabled'
p_output_box.grid(row=2, column=1, sticky="nsew")
p_output_box.tag_config("even")

# Create a Scrollbars widgets for program output window
# y scrollbar
p_scrollbar_y = tk.Scrollbar(tab1)
p_scrollbar_y.grid(row=2, column=2, sticky="nsew")
# x scrollbar
p_scrollbar_x = tk.Scrollbar(tab1, orient="horizontal")
p_scrollbar_x.grid(row=3, column=1, sticky="nsew")

# Configure the program output window widget to use the Scrollbars
p_output_box.config(yscrollcommand=p_scrollbar_y.set)
p_scrollbar_y.config(command=p_output_box.yview)

p_output_box.config(xscrollcommand=p_scrollbar_x.set)
p_scrollbar_x.config(command=p_output_box.xview)

# Create a button to copy the v boudach query output
b_copy_output_button = tk.Button(tab1, text="↓ COPY Found in monuments ↓", command=copy_boudy_output, width=20, font=("Verdana", 11, "bold"), background="gray", foreground="white")
b_copy_output_button.grid(row=5, column=1, sticky="nsew")

# Create an output box for the v boudach query result
b_output_box = tk.Text(tab1, wrap="none", borderwidth=1, background="dark gray", foreground="black", relief="solid")
b_output_box['state'] = 'disabled'
b_output_box.grid(row=6, column=1, sticky="nsew")

# Create a Scrollbars widgets for v monumentech output window
# y scrollbar
b_scrollbar_y = tk.Scrollbar(tab1)
b_scrollbar_y.grid(row=6, column=2, sticky="nsew")
# x scrollbar
b_scrollbar_x = tk.Scrollbar(tab1, orient="horizontal")
b_scrollbar_x.grid(row=7, column=1, sticky="nsew")

# Configure the monuments output window widget to use the Scrollbars
b_output_box.config(yscrollcommand=b_scrollbar_y.set)
b_scrollbar_y.config(command=b_output_box.yview)

b_output_box.config(xscrollcommand=b_scrollbar_x.set)
b_scrollbar_x.config(command=b_output_box.xview)

# Create a button to run the programs query
p_run_query_button = tk.Button(tab1, text="SHOW programs\n[ENTER]", command=run_queries, font=("Verdana", 11, "bold"), background="gray", foreground="white", relief="solid")
p_run_query_button.grid(row=3, rowspan=3, column=0, sticky="nsew")

# Create a button to clear all widgets
clear_button = tk.Button(tab1, text="CLEAR\n[DEL]", command=clear_everything, font=("Verdana", 11, "bold"), background="gray", foreground="white")
clear_button.grid(row=6, column=0, sticky="nsew")

##### END 1st tab

##### Create 2nd tab
tab2 = ttk.Frame(notebook)

# This makes collumns in tab to expand and fill available sapce when window is resized
tab2.columnconfigure(0, minsize=170, weight=1)
tab2.columnconfigure(2, minsize=170, weight=1)

### Manual addidg / deleting

# Label manual inputs
tab2_l = tk.Label(tab2, font=font, text="↓ Manual add / delete BOM record ↓", background="black", foreground="white", borderwidth=0, relief="solid", padx=3 ,pady=5)
tab2_l.grid(row=0, rowspan=1, column=0, columnspan=3, sticky="nesw")

## PN + in monument labels
# pn label
tab2_l_pn = tk.Label(tab2, font=font2, text="Part number",anchor="w", background="gray", foreground="white", borderwidth=0, relief="solid", pady=5)
tab2_l_pn.grid(row=1, column=0, columnspan=2, sticky="nesw")

# in monumetns label
tab2_l_im = tk.Label(tab2, font=font2, text="In monument",anchor="w", background="gray", foreground="white", borderwidth=0, relief="solid", pady=5)
tab2_l_im.grid(row=1, column=2, sticky="nesw")

# Search window for PN
tab2_t_pn = tk.Text(tab2, font=font2, height=1)
# t_pn = tk.Text(tab2, font=font2, height=1, width=30 )
tab2_t_pn.grid(row=2, column=0, sticky="nesw", pady=1)

# sep label
tab2_s_l = tk.Label(tab2, height=1)
tab2_s_l.grid(row=2, column=1,  sticky="news", pady=1) 

# Search window for in monument
tab2_t_im = tk.Text(tab2, font=font2, height=1)
#t_im = tk.Text(tab2, font=font2, height=1, width=30 )
tab2_t_im.grid(row=2, column=2, sticky="nesw", pady=1)

# Add pn search button
tab2_pn_search_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\search33.png')
tab2_pn_search_button = tk.Button(tab2, image=tab2_pn_search_icon, background="gray", command=lambda: search_pn_in_monument(database_path, tab2_t_pn.get(1.0, tk.END), tab2_t_im.get(1.0, tk.END)))
#select_cq_button = tk.Button(tab2, text="↓ SELECT FILE ↓", command=select_cq_file, font=("Verdana", 11, "bold"), background="gray", foreground="white")
tab2_pn_search_button.grid(row=3, column=0, pady=2, sticky="w")

# Add pn search clear button
tab2_clear_search_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\clear_search33.png')
tab2_clear_search_button = tk.Button(tab2, image=tab2_clear_search_icon, background="gray", command=clear_pn_in_monument_search)
#select_cq_button = tk.Button(tab2, text="↓ SELECT FILE ↓", command=select_cq_file, font=("Verdana", 11, "bold"), background="gray", foreground="white")
tab2_clear_search_button.grid(row=3, column=0, pady=2, sticky="w", padx=30)

# Add a message label
tab2_l_message= tk.Label(tab2, font=("Verdana", 11, "bold"),  background=root['bg'], text="")
tab2_l_message.grid(row=3, column=0, columnspan=3, pady=2, padx=60, sticky="nsew")

# Add action button to add / delete record 
tab2_button_action_record = tk.Button(tab2, width=6, relief="sunken", bd=0)
tab2_button_action_record.grid(row=3, column=2, columnspan=1, pady=2 , padx=0, sticky="nse")

###  A. CQ file updates

# Add CQ updates label
tab2_l = tk.Label(tab2, font=font, text="↓ CQ file BOM update ↓", background="black", foreground="white", borderwidth=0, relief="solid", padx=3 ,pady=5)
tab2_l.grid(row=4, rowspan=1, column=0, columnspan=3, sticky="nesw") 

# Create a label for CQ txt file selection
tab2_select_cq_file_label = tk.Label(tab2, text=
'''
1. Select CQ report txt file containing BOMs
of monuments, you want to add to database.
'''
, font=font2, background="gray", foreground="white", borderwidth=0, relief="solid", padx=10)
tab2_select_cq_file_label.grid(row=5, column=0, columnspan=3, sticky="news")
 
# Create button to select cq filepath
tab2_cq_file_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\cq_openfile.png')
tab2_select_cq_button = tk.Button(tab2, image=tab2_cq_file_icon, background="gray", command=select_cq_file)
#select_cq_button = tk.Button(tab2, text="↓ SELECT FILE ↓", command=select_cq_file, font=("Verdana", 11, "bold"), background="gray", foreground="white")
tab2_select_cq_button.grid(row=6, column=0, sticky="w")

# Create text box to show path to cq file
tab2_cq_file_path_box = tk.Text(tab2,wrap="none", height=1  ,borderwidth=1, font=font2, background="dark gray", foreground="black", relief="solid", padx=5)
tab2_cq_file_path_box['state'] = 'disabled'
tab2_cq_file_path_box.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=(30,0))
 
# Create a label for CQ txt file to be processed and parts added to database
tab2_add_from_cq_label = tk.Label(tab2, text=
'''
2. Then click on button bellow to process CQ report
txt file containing BOMs of monuments and add
monuments from it to database.
'''
, font=font2, background="gray", foreground="white", borderwidth=0, relief="solid", padx=10)
tab2_add_from_cq_label.grid(row=7, column=0, columnspan=3, sticky="news")
# 
# Create button to process the selected file
tab2_cq_process_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\cq_into_db.png')
tab2_process_cq_button = tk.Button(tab2, image=tab2_cq_process_icon, background="gray", command=lambda: process_cq_file(database_path, tab2_cq_file_path_box.get(1.0, tk.END).replace("\n","")), width=62, height=62)
tab2_process_cq_button.grid(row=8, column=1)

###  B. txt file updates

# Add txt file updates label
tab2_l = tk.Label(tab2, font=font, text="↓ TXT file BOM update ↓", background="black", foreground="white", borderwidth=0, relief="solid", padx=3 ,pady=5)
tab2_l.grid(row=9, rowspan=1, column=0, columnspan=3, sticky="nesw")

# Create a label for txt file selection
tab2_select_txt_file_label = tk.Label(tab2, text=
'''
1. Select txt file containing pairs of part numbers and monuents
in which these part numbers are found.
- Values must be separated by TAB.
- First line of file must contain heading.
These pairs will be added to the BOM database.
'''
, font=font2, background="gray", foreground="white", borderwidth=0, relief="solid", padx=10)
tab2_select_txt_file_label.grid(row=10, column=0, columnspan=3, sticky="news")

# Create button to select txt filepath
tab2_txt_file_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\txt_openfile.png')
tab2_select_txt_button = tk.Button(tab2, image=tab2_txt_file_icon, background="gray", command=select_txt_file)
tab2_select_txt_button.grid(row=11, column=0, sticky="w")

# Create text box to show path to txt file
tab2_txt_file_path_box = tk.Text(tab2, wrap="none", height=1  ,borderwidth=1, font=font2, background="dark gray", foreground="black", relief="solid", padx=5)
tab2_txt_file_path_box['state'] = 'disabled'
tab2_txt_file_path_box.grid(row=11, column=0, columnspan=3, sticky="nsew", padx=(30,0))

# Create a label for CQ txt file to be processed and parts added to database
tab2_add_from_txt_label = tk.Label(tab2, text=
'''
2. Then click on button bellow to process txt file containing
pairs of PN:MONUMENT to be added into the database.
'''
, font=font2, background="gray", foreground="white", borderwidth=0, relief="solid", padx=10)
tab2_add_from_txt_label.grid(row=12, column=0, columnspan=3, sticky="news")

# Create button to process the selected file
tab2_txt_process_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\txt_into_db.png')
tab2_process_txt_button = tk.Button(tab2, image=tab2_txt_process_icon, background="gray", command=lambda: bom_process_txt_file(database_path, tab2_txt_file_path_box.get(1.0, tk.END).replace("\n","")), width=62, height=62)
#select_cq_button = tk.Button(tab2, text="↓ SELECT FILE ↓", command=select_cq_file, font=("Verdana", 11, "bold"), background="gray", foreground="white")
tab2_process_txt_button.grid(row=13, column=1)

##### END 2 nd tab

##### Create 3rd tab
tab3 = ttk.Frame(notebook)

# This makes collumns in tab to expand and fill available sapce when window is resized
tab3.columnconfigure(0, minsize=100, weight=1)
tab3.columnconfigure(2, minsize=100, weight=1)
tab3.columnconfigure(4, minsize=70, weight=0)
tab3.columnconfigure(6, minsize=100, weight=1)

### A Manual addidg / deleting

# Label manual inputs
tab3_l = tk.Label(tab3, font=font, text="↓ Manual add / delete MONUMENT PROGRAM record ↓", background="blue", foreground="white", borderwidth=0, relief="solid", padx=3 ,pady=5)
tab3_l.grid(row=0, rowspan=1, column=0, columnspan=7, sticky="nesw")

## Monument labels
# Monument label
tab3_l_m = tk.Label(tab3, font=font2, text="Monument",anchor="w", background="blue", foreground="white", borderwidth=0, relief="solid", pady=5)
tab3_l_m.grid(row=1, column=0, columnspan=2, sticky="nesw")

# Description label
tab3_l_d = tk.Label(tab3, font=font2, text="Description",anchor="w", background="blue", foreground="white", borderwidth=0, relief="solid", pady=5)
tab3_l_d.grid(row=1, column=2, columnspan=2, sticky="nesw")

# Program label
tab3_l_p = tk.Label(tab3, font=font2, text="Program",anchor="w", background="blue", foreground="white", borderwidth=0, relief="solid", pady=5)
tab3_l_p.grid(row=1, column=4, columnspan=2, sticky="nesw")

# Specific rules label
tab3_l_sr = tk.Label(tab3, font=font2, text="Specific rules",anchor="w", background="blue", foreground="white", borderwidth=0, relief="solid", pady=5)
tab3_l_sr.grid(row=1, column=6, columnspan=2, sticky="nesw")

## Search windows

# Search window for monument
tab3_t_m = tk.Text(tab3, font=font2, height=1)
tab3_t_m.grid(row=2, column=0, sticky="nesw", pady=1)

# sep label
tab3_s_l = tk.Label(tab3, height=1)
tab3_s_l.grid(row=2, column=1,  sticky="news", pady=1) 

# Search window for Description
tab3_t_d = tk.Text(tab3, font=font2, height=1, background="gray", foreground="white")
tab3_t_d.grid(row=2, column=2, sticky="nesw", pady=1)
tab3_t_d['state'] = 'disabled'

# sep label
tab3_s_l = tk.Label(tab3, height=1)
tab3_s_l.grid(row=2, column=3,  sticky="news", pady=1) 

# Search window for Program
tab3_t_p = tk.Text(tab3, font=font2, height=1 ,width=10, background="gray", foreground="white")
tab3_t_p.grid(row=2, column=4, sticky="nesw", pady=1)
tab3_t_p['state'] = 'disabled'

# sep label
tab3_s_l = tk.Label(tab3, height=1)
tab3_s_l.grid(row=2, column=5,  sticky="news", pady=1) 

# Search window for Specific rules
tab3_t_sr = tk.Text(tab3, font=font2, height=1, background="gray", foreground="white")
tab3_t_sr.grid(row=2, column=6, sticky="nesw", pady=1)
tab3_t_sr['state'] = 'disabled'

# Manual buttons and messages

# Add pn search button
tab3_pn_search_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\search33.png')
tab3_pn_search_button = tk.Button(tab3, image=tab3_pn_search_icon, background="gray", command=lambda: search_for_monument(database_path, tab3_t_m.get(1.0,tk.END)))
tab3_pn_search_button.grid(row=3, column=0, pady=2, sticky="w")

# Add pn search clear button
tab3_clear_search_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\clear_search33.png')
tab3_clear_search_button = tk.Button(tab3, image=tab3_clear_search_icon, background="gray", command=clear_monument_search)
tab3_clear_search_button.grid(row=3, column=0, pady=2, sticky="w", padx=30)
 
# Add a message label
tab3_l_message= tk.Label(tab3, font=("Verdana", 11, "bold"),  background=root['bg'], text="")
tab3_l_message.grid(row=3, column=0, columnspan=7, pady=2, padx=(60,120), sticky="nsew")

# Add action button to add / delete record 
tab3_button_action_record = tk.Button(tab3, width=10, relief="sunken", bd=0, background=root['bg'])
tab3_button_action_record.grid(row=3, column=6, columnspan=1, pady=2 , padx=0, sticky="nse")

# Add action button to update record 
tab3_button_update_record = tk.Button(tab3, width=10, relief="sunken", bd=0, background=root['bg'])
tab3_button_update_record.grid(row=3, column=6, columnspan=1, pady=2 , padx=(0,70), sticky="nse")
 
###  B. txt file updates

# Add txt file updates label
tab3_l = tk.Label(tab3, font=font, text="↓ TXT file MONUMENT PROGRAM update ↓", background="blue", foreground="white", borderwidth=0, relief="solid", padx=3 ,pady=5)
tab3_l.grid(row=4, rowspan=1, column=0, columnspan=7, sticky="nesw")

# Create a label for txt file selection
tab3_select_txt_file_label = tk.Label(tab3, text=
'''
1. Select txt file containing Monuments and their data.
- Values in file MUST be in same order as in Manual section above.
- Data columns in file MUST be sepparated by TAB.
- First line of file must contain heading.
These monuments and their data will be added to the MONUMENT database.
'''
, font=font2, background="light blue", foreground="black", borderwidth=0, relief="solid", padx=10)
tab3_select_txt_file_label.grid(row=5, column=0, columnspan=7, sticky="news")

# Create button to select txt filepath
tab3_txt_file_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\txt_openfile.png')
tab3_select_txt_button = tk.Button(tab3, image=tab3_txt_file_icon, background="gray", command=tab3_select_txt_file)
tab3_select_txt_button.grid(row=6, column=0, sticky="w")

# Create text box to show path to txt file
tab3_txt_file_path_box = tk.Text(tab3, wrap="none", height=1  ,borderwidth=1, font=font2, background="dark gray", foreground="black", relief="solid", padx=5)
tab3_txt_file_path_box['state'] = 'disabled'
tab3_txt_file_path_box.grid(row=6, column=0, columnspan=7, sticky="nsew", padx=(30,0))

# Create a label for txt file to be processed and monuments from it added to database
tab3_add_from_txt_label = tk.Label(tab3, text=
'''
2. Then click on button bellow to process txt file containing
MONUMENTs and their data to be added into the database.
'''
, font=font2, background="light blue", foreground="black", borderwidth=0, relief="solid", padx=10)
tab3_add_from_txt_label.grid(row=7, column=0, columnspan=7, sticky="news")

# Create button to process the selected file
tab3_txt_process_icon = tk.PhotoImage(file=f'{current_folder_path}\\graphics\\txt_into_db.png')
tab3_process_txt_button = tk.Button(tab3, image=tab3_txt_process_icon, background="gray", command=lambda:monuments_process_txt_file(database_path, tab3_txt_file_path_box.get(1.0, tk.END)), width=62, height=62)
#select_cq_button = tk.Button(tab2, text="↓ SELECT FILE ↓", command=select_cq_file, font=("Verdana", 11, "bold"), background="gray", foreground="white")
tab3_process_txt_button.grid(row=8, column=2, sticky="e")

##### END 3 rd tab

# Add tabs to notebook
notebook.add(tab1, text=" SFE x BFE x MIX ")
notebook.add(tab2, text="  BOM databáze ")
notebook.add(tab3, text="  PROGRAMY databáze ")
#notebook.add(tab3, text="  programy databáze ")

# Pack notebook to root
notebook.pack(fill="both", expand=True)

### Event bindings
# Bind the tab select event to the tab_select function
notebook.bind("<<NotebookTabChanged>>", tab_select)

# Run the main loop
root.mainloop()