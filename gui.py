import random
import tkinter as tk
import re
import pandas as pd
from tkinter import END, messagebox

# load the word list
df = pd.read_excel('dead_db.xlsx')
my_list = df["Name"].tolist()
target_word = random.choice(my_list)
print(target_word)


# set up the main window
my_w = tk.Tk()
my_w.geometry("500x500")
my_w.title("deadle")
font1 = ("Times", 24, 'bold')


# UI elements

e1_str = tk.StringVar()
e1 = tk.Entry(my_w, font=font1, textvariable=e1_str)
e1.grid(row=0, column=1, padx=20, pady=0)

l1 = tk.Listbox(my_w, height=10, font=font1, relief='flat',
                bg='SystemButtonFace', highlightcolor='SystemButtonFace')
l1.grid(row=2, column=1)

def get_data(*args):
    search_str = e1.get()
    l1.delete(0, END)
    for element in my_list:
        element_str = str(element)
        if re.match(search_str, element_str, re.IGNORECASE):
            l1.insert(tk.END, element)


def my_upd(event):
    try:
        index = l1.curselection()[0]
        value = l1.get(index)
        e1_str.set(value)
        l1.delete(0, END)
    except IndexError:
        raise "index error"


l1.bind("<<ListBoxSelect>>", my_upd)
e1_str.trace('w', get_data)

feedback_label = tk.Label(my_w, font=font1)
feedback_label.grid(row=3, column=1, padx=20, pady=20)


# Function to process guesses
def process_guess():
    guess = e1_str.get().upper()
    if len(guess) != len(target_word):
        messagebox.showinfo("Error", "Guess must be the same length as the target word.")
        return
    feedback = ""
    for g, t in zip(guess, target_word):
        if g == t:
            feedback += "🟩"
        elif g in target_word:
            feedback += "🟨"
        else:
            feedback += "⬛"
    feedback_label.config(text=feedback)
    e1.delete(0, END)
    if guess == target_word:
        messagebox.showinfo("Congratulations!", "You've guessed the word correctly!")

# Guess button
guess_button = tk.Button(my_w, text="Guess", font=font1, command=process_guess)
guess_button.grid(row=1, column=1, pady=20)

my_w.mainloop()
