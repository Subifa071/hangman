from tkinter import *
from tkinter import messagebox
from string import ascii_uppercase
import random
import pygame
from pygame import mixer

window = Tk()
window.title("Hangman")
window.iconbitmap("death.ico")
window.resizable(width=False, height=False)
pygame.mixer.pre_init(3400, -16, 1, 512)
mixer.init()
pygame.init()

#sounds
win_fx = pygame.mixer.Sound("win.wav")
win_fx.set_volume(50)

lose_fx = pygame.mixer.Sound("lose.wav")
lose_fx.set_volume(50)

word_list=["RUSSIA", "ARGENTINA", "MEXICO", "COLOMBIA", "KAZAKHSTAN", "GERMANY", "TURKEY", "HUNGARY", "FINLAND",
             "INDIA", "CHINA", "SWEDEN",
             "MONGOLIA", "MOROCCO", "NORWAY", "CHILE", "IRELAND", "ICELAND", "CROATIA", "ESTONIA", "SPAIN", "NIGERIA",
             "JAPAN", "UKRAINE", "ALGERIA"]

"""word_list = []
with open("words.txt") as f:
    for line in f:
        word_list.append(line.strip())"""


photos = (PhotoImage(file="hang0.png"), PhotoImage(file="hang1.png"), PhotoImage(file="hang2.png"),
PhotoImage(file="hang3.png"),
PhotoImage(file="hang4.png"), PhotoImage(file="hang5.png"), PhotoImage(file="hang6.png"),
PhotoImage(file="hang7.png"),
PhotoImage(file="hang8.png"), PhotoImage(file="hang9.png"),
PhotoImage(file="hang10.png"), PhotoImage(file="hang11.png"))


def newGame():
    global the_word_withSpaces
    global numberOfGuesses
    numberOfGuesses = 0  # intialize
    imgLabel.config(image=photos[0])  # config = display images
    the_word = random.choice(word_list)
    the_word_withSpaces = " ".join(the_word)  # or else wont work
    lblWord.set(" ".join("_" * len(the_word)))  # for dash lines


def guess(letter):
    global numberOfGuesses
    if numberOfGuesses < 11:
        txt = list(the_word_withSpaces)
        guessed = list(lblWord.get())  # if correct letter print on top of dash
        if the_word_withSpaces.count(letter) > 0:
            for c in range(
                    len(txt)):  # wont print letter on top of dash, remains blank if the guessed letter is true & if not hangman is drawn
                if txt[c] == letter:
                    guessed[c] = letter
            lblWord.set("".join(guessed))
            if lblWord.get() == the_word_withSpaces:
                win_fx.play()
                messagebox.showinfo("Hangman", "You guessed it!")
                newGame()

        else:
            numberOfGuesses += 1
            imgLabel.config(image=photos[numberOfGuesses])
            if numberOfGuesses == 11:
                lose_fx.play()
                messagebox.showwarning("Hangman", "Game Over")


# GUI
imgLabel = Label(window)
imgLabel.grid(row=0, column=0, columnspan=3, padx="10", pady="40")
imgLabel.config(image=photos[0])
lblWord = StringVar()
Label(window,fg="green", textvariable=lblWord, font=("Consolas 24 bold")).grid(row=0, column=3, columnspan=6, padx="10")

# goes through all 26 alphabets
n = 0
for c in ascii_uppercase:
    Button(window,bg="bisque", text=c, command=lambda c=c: guess(c), font=("Helvetica 18"), width=4).grid(row=1 + n // 9,
                                                                                              column=n % 9)
    n += 1

Button(window,bg="rosybrown",text="New\nGame", command=lambda: newGame(), font=("Helvetica 10 bold")).grid(row=3, column=8,
                                                                                             sticky="NSWE")

newGame()
mainloop()
