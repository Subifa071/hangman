import tkinter
from tkinter import *
from tkinter import messagebox
import sys
from hangman import newGame

root = tkinter.Toplevel()
root.title("H_ngm_n")
root.iconbitmap("death.ico")
root.geometry("800x600")
root.resizable(width=False, height=False)
bg = PhotoImage(file="hangman_background.png")

# Creating Canvas
my_canvas = Canvas(root, width=800, height=600, highlightthickness=0)
my_canvas.pack(fill="both", expand=False)

#Setting Canvas Image
my_canvas.create_image(0,0, image=bg, anchor="nw")


#Defining Exit Button
def alert():
        sure_exit = messagebox.askyesno("Exit", "Are You Sure To Exit The Game?")

        if sure_exit == 1:
            sys.exit()
        else:
            pass


#Creating Start Button
start_button = Button(root, text="START",  bd=0, bg="wheat",fg="black", font=("Chocolate Covered Raindrops Bol", 22, 'bold'), width=15, height=2,command = newGame)
start_window = my_canvas.create_window(210, 150, anchor="nw", window=start_button)


#Creating Sound Button
sound_button = Button(root, text="SOUND", bg="wheat", bd=0, fg="black", font=("Chocolate Covered Raindrops Bol", 22, 'bold'), width=15, height=2)
sound_window = my_canvas.create_window(210, 250, anchor="nw", window=sound_button)

#Creating Exit Button
exit_button = Button(root, text="EXIT",bg="wheat",bd=0, fg="black", font=("Chocolate Covered Raindrops Bol", 22, 'bold'), width=15, height=2, command=alert)
exit_window = my_canvas.create_window(210, 350, anchor="nw", window=exit_button)

root.mainloop()
