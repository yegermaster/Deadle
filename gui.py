import tkinter as tk
import re
from tkinter import END
import pandas as pd

my_w = tk.Tk()
my_w.geometry("500x500")
my_w.title("wordle")
font1 = ("Times", 24, 'bold')
df = pd.read_excel('new.xlsx')
my_list = df["Name"].tolist()

def my_upd(my_widget):
    my_w = my_widget.widget
    index = int(my_w.curselection()[0])
    value = my_w.get(index)
    e1_str.set(value)
    l1.delete(0, END)



e1_str = tk.StringVar()
e1 = tk.Entry(my_w, font=font1, textvariable=e1_str)
e1.grid(row=0, column=1, padx=20, pady=0)
l1 = tk.Listbox(my_w, height=10, font=font1, relief='flat',
                bg='SystemButtonFace', highlightcolor='SystemButtonFace')
l1.grid(row=1, column=1)

def get_data(*args):
    search_str = e1.get()
    l1.delete(0, END)
    for element in my_list:
        element_str = str(element)
        if re.match(search_str, element_str, re.IGNORECASE):
            l1.insert(tk.END, element)

l1.bind("<<ListBoxSelect>>", my_upd)


e1_str.trace('w', get_data)

my_w.mainloop()

