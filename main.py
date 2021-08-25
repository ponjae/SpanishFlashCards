from tkinter import *
import pandas
from random import choice

from pandas.core import indexing

BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/spanish600.csv")
data_dict = data.to_dict(orient="records")
current_card = {}

# ---------------------------- WORD FUNCTIONS ------------------------------- #


def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(data_dict)
    spanish = current_card["Spanish"]
    card_canvas.itemconfig(title, text="Spanish", fill="black")
    card_canvas.itemconfig(word, text=spanish, fill="black")
    card_canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=show_translation)


def show_translation():
    card_canvas.itemconfig(card_background, image=card_back)
    card_canvas.itemconfig(title, text="English", fill="white")
    card_canvas.itemconfig(word, text=current_card["English"], fill="white")


def is_known():
    data_dict.remove(current_card)
    data = pandas.DataFrame(data_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    new_word()


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("My Flash Card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=show_translation)

# The card
card_canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_background = card_canvas.create_image(400, 263, image=card_front)
card_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title = card_canvas.create_text(400, 150, text="Spanish",
                                font=("Ariel", 40, "italic"))
word = card_canvas.create_text(
    400, 263, text="Hola", font=("Ariel", 60, "bold"))
card_canvas.grid(row=0, column=0, columnspan=2)

# Buttons
correct_img = PhotoImage(file="images/right.png")
incorrect_img = PhotoImage(file="images/wrong.png")
correct_btn = Button(image=correct_img, highlightthickness=0,
                     border=0, command=is_known)
incorrect_btn = Button(image=incorrect_img,
                       highlightthickness=0, border=0, command=new_word)

correct_btn.grid(row=1, column=0)
incorrect_btn.grid(row=1, column=1)

word_dict = new_word()

window.mainloop()
