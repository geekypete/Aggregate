from Tkinter import *

root = Tk()

scrollbar2 = Scrollbar(root, orient=HORIZONTAL)
scrollbar2.grid(row=1,column=0, sticky=E+W)

scrollbar = Scrollbar(root, orient=VERTICAL)
scrollbar.grid(row=0, column=1, sticky=N+S)

listbox = Listbox(root, xscrollcommand=scrollbar2.set, yscrollcommand=scrollbar.set)
listbox.grid(row=0, column=0)

for i in range(100):
    listbox.insert(END, i+10000000000000000000000)

# attach listbox to scrollbar
scrollbar.config(command=listbox.yview)
scrollbar2.config(command=listbox.xview)

mainloop()