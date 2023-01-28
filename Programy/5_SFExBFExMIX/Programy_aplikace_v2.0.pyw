import tkinter as tk
from tkinter import ttk
import os
import time
from SQL_update.Modules import queries, sqllite

### Setup files

# Nalezeni stavajiciho umisteni
current_folder_path = os.path.dirname(os.path.abspath(__file__))
# Nazev databaze, kam chceme vkladat zaznamy
database_name = 'programy.db'
# Sestaveni cesty databaze (predpoklada, ze se databaze nachazi v podslozce SQL_update ve slozce programu.)
database_path = f'{current_folder_path}\\SQL_update\\{database_name}'

# Nazvy tabulek v databazi
pns = "part_numbers"
dXb = "dilyXboudy"
bXp = "boudyXprogramy"

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

### CREATE THE MAIN WINDOW
root = tk.Tk()

root.title("Ukazovadlo programů SFE x BFE x MIX")
root.iconbitmap("Y:\\Departments\\Sales and Marketing\\Aftersales\\11_PLANNING\\23_Python_utilities\\5_SFExBFExMIX\\graphics\\icon.ico")
root.geometry('900x600+0+3')

# FONT
font = ("Verdana", 12, "bold")

# Button style
style = ttk.Style()
style.configure("TButton", font=("Verdana", 11, "bold"), foreground="black")

# Configure specific columns and rows for correct resizing

root.columnconfigure(0, minsize=100, weight=1)
root.columnconfigure(1, minsize=100, weight=10)

root.rowconfigure(2, minsize=100, weight=1)
root.rowconfigure(6, minsize=200, weight=10)

# Create a label for the part number input
part_number_label = tk.Label(root, text="↓ Enter part numbers ↓", font=font)
part_number_label.grid(row=0, rowspan=2, column=0, sticky="nsew")

# Create a button to copy the programs query output
p_copy_output_button = ttk.Button(root, text="↓ COPY result programs ↓", command=copy_programy_output, style="TButton")
p_copy_output_button.grid(row=0, column=1, sticky="nsew")

# Create a entry box for the part number input
entry_box = tk.Text(root, wrap="none", borderwidth=3, width=15, height=10)
entry_box.grid(row=2, column=0, sticky="nsew")
 
# Create an output box for the programs query result
# p_output_box = tk.Text(root,width=130, borderwidth=3)
p_output_box = tk.Text(root, wrap="none", borderwidth=3, height=1)
p_output_box['state'] = 'disabled'
p_output_box.grid(row=2, column=1, sticky="nsew")
p_output_box.tag_config("even")

# Create a Scrollbars widgets for program output window
# y scrollbar
p_scrollbar_y = tk.Scrollbar(root)
p_scrollbar_y.grid(row=2, column=2, sticky="nsew")
# x scrollbar
p_scrollbar_x = tk.Scrollbar(root, orient="horizontal")
p_scrollbar_x.grid(row=3, column=1, sticky="nsew")

# Configure the program output window widget to use the Scrollbars
p_output_box.config(yscrollcommand=p_scrollbar_y.set)
p_scrollbar_y.config(command=p_output_box.yview)

p_output_box.config(xscrollcommand=p_scrollbar_x.set)
p_scrollbar_x.config(command=p_output_box.xview)

# Create a button to copy the v boudach query output
b_copy_output_button = ttk.Button(root, text="↓ COPY Found in monuments ↓", command=copy_boudy_output, width=20, style="TButton")
b_copy_output_button.grid(row=5, column=1, sticky="nsew")

# Create an output box for the v boudach query result
b_output_box = tk.Text(root, wrap="none", borderwidth=3)
b_output_box['state'] = 'disabled'
b_output_box.grid(row=6, column=1, sticky="nsew")

# Create a Scrollbars widgets for v monumentech output window
# y scrollbar
b_scrollbar_y = tk.Scrollbar(root)
b_scrollbar_y.grid(row=6, column=2, sticky="nsew")
# x scrollbar
b_scrollbar_x = tk.Scrollbar(root, orient="horizontal")
b_scrollbar_x.grid(row=7, column=1, sticky="nsew")

# Configure the monuments output window widget to use the Scrollbars
b_output_box.config(yscrollcommand=b_scrollbar_y.set)
b_scrollbar_y.config(command=b_output_box.yview)

b_output_box.config(xscrollcommand=b_scrollbar_x.set)
b_scrollbar_x.config(command=b_output_box.xview)

# Create a button to run the programs query
p_run_query_button = ttk.Button(root, text="SHOW programs\n[ENTER]", command=run_queries, style="TButton")
p_run_query_button.grid(row=3, rowspan=3, column=0, sticky="nsew")

# Create a button to clear all widgets
clear_button = ttk.Button(root, text="CLEAR\n[DEL]", command=clear_everything, style="TButton")
clear_button.grid(row=6, column=0, sticky="nsew")

### KEY BINDINGS

# Run both queries on ENTER pressed
root.bind("<Return>", key_run_queries)
# Clear all text on DEL pressed
root.bind("<Key-Delete>", key_clear_everything)


# Run the main loop
root.update()
root.mainloop()
