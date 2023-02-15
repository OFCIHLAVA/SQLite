import tkinter as tk
from tkinter import ttk

root = tk.Tk()

notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)

# create a canvas to display the contents of the tab
canvas = tk.Canvas(tab1)
canvas.pack(side="left", fill="both", expand=True)

# create a scrollbar and connect it to the canvas
scrollbar = tk.Scrollbar(tab1, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# create a frame to contain the contents of the tab
frame = tk.Frame(canvas, background="green")
canvas.create_window((0, 0), window=frame, anchor="nw")

# add some widgets to the frame
for i in range(50):
    tk.Label(frame, text="Label {}".format(i)).pack()

# make sure the frame is the correct size
frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

notebook.add(tab1, text="Tab 1")
notebook.pack(fill="both", expand=True)

root.mainloop()