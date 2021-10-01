import random
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pygame

# Window settings
root = Tk()
root.title("H_NGM_N")
root.iconbitmap("death.ico")
root.geometry("800x400")
root.resizable(width=False, height=False)

def disable_event():
    pass

pygame.mixer.init(44000, -16, 2, 512)
music_state = False

def play_music():
    global music_state
    if music_state:
        pygame.mixer.music.stop()

    else:
        pygame.mixer.music.load("game.mp3")
        pygame.mixer.music.play(loops=0)
        music_state = not music_state  # if it is in the same line of else music wont stop even if we close tha game


def main_menu_():
    root.deiconify()

    global main_menu_bg

    global letter_change
    letter_change = 1
    global word_change
    word_change = 2

    # Create canvas and add background
    canvas = Canvas(root, width="800", height="450")
    canvas.pack()

    main_menu_bg = ImageTk.PhotoImage(Image.open("home_background.png").resize((800, 450), Image.ANTIALIAS))
    canvas.background = main_menu_bg
    canvas.create_image(0, 0, anchor=NW, image=main_menu_bg)

    # Add buttons to canvas
    start_btn = Button(root, text="New Game", bg="bisque", width=25, command=new_game, borderwidth=5)
    canvas.create_window(500, 150, anchor=E, window=start_btn)

    score_btn = Button(root, text="Score Board", bg="bisque", width=25, command=score_board, borderwidth=5)
    canvas.create_window(500, 210, anchor=E, window=score_btn)

    quit_btn = Button(root, text="Quit", bg="bisque", width=25, command=quit_game, borderwidth=5)
    canvas.create_window(500, 270, anchor=E, window=quit_btn)

    sound_btn = Button(root, text="Sound", command=play_music)
    canvas.create_window(770, 380, anchor=SE, window=sound_btn)


def new_game():
    root.withdraw()  # Hide root window, to make it visible again use root.deiconify()

    global new_game_bg
    global new_game_window

    new_game_window = Toplevel()
    new_game_window.title("HangMan")
    new_game_window.iconbitmap("death.ico")
    new_game_window.geometry("800x400")
    new_game_window.resizable(width=False, height=False)
    new_game_window.protocol("WM_DELETE_WINDOW", disable_event)  # Disable window "X" (close) button

    # Create canvas and add background
    canvas_new_game = Canvas(new_game_window, width="800", height="450")
    canvas_new_game.pack()

    new_game_bg = ImageTk.PhotoImage(Image.open("choices.png").resize((800, 450), Image.ANTIALIAS))
    canvas_new_game.background = new_game_bg
    canvas_new_game.create_image(0, 0, anchor=NW, image=new_game_bg)

    instructions_lbl = Label(new_game_window, text="There are 4 different categories.\n"
                                                   "Choose as many as you'd like,"
                                                   "\nbut do choose wisely, this is not going to be easy!",
                             bg="#a5a0b6")
    canvas_new_game.create_window(400, 60, anchor=CENTER, window=instructions_lbl)

    # Will help knowing which categories were chosen
    var1 = StringVar(value="")
    var2 = StringVar(value="")
    var3 = StringVar(value="")
    var4 = StringVar(value="")

    books_btn = Checkbutton(new_game_window, text="Books", variable=var1, onvalue="b", offvalue="")
    canvas_new_game.create_window(340, 120, anchor=CENTER, window=books_btn)
    games_btn = Checkbutton(new_game_window, text="Games", variable=var2, onvalue="g", offvalue="")
    canvas_new_game.create_window(440, 120, anchor=CENTER, window=games_btn)
    movies_btn = Checkbutton(new_game_window, text="Movies", variable=var3, onvalue="m", offvalue="")
    canvas_new_game.create_window(340, 170, anchor=CENTER, window=movies_btn)
    tv_btn = Checkbutton(new_game_window, text="TV-Shows", variable=var4, onvalue="t", offvalue="")
    canvas_new_game.create_window(440, 170, anchor=CENTER, window=tv_btn)

    start_new_game_btn = Button(new_game_window, text="Start new game", width=15,
                                command=lambda: [prepare(var1.get() + var2.get() + var3.get() + var4.get())]
                                , borderwidth=5)
    canvas_new_game.create_window(390, 220, anchor=CENTER, window=start_new_game_btn)

    back_menu_btn = Button(new_game_window, text="Main Menu", width=15, command=lambda: [main_menu_(),
                                                                                         new_game_window.destroy()]
                           , borderwidth=5)
    canvas_new_game.create_window(390, 260, anchor=CENTER, window=back_menu_btn)

    quit_game_btn = Button(new_game_window, text="Quit game", width=15, command=quit_game)
    canvas_new_game.create_window(390, 300, anchor=CENTER, window=quit_game_btn)

    sound_btn = Button(new_game_window, text="Sound", command=play_music)
    canvas_new_game.create_window(770, 380, anchor=CENTER, window=sound_btn)


# choice variable will contain the user's wanted category for the game
def prepare(choice):
    global count_lines

    # Create file of words
    movies = open("movies list.txt", "r")  # Open word files
    games = open("games list.txt", "r")
    tv = open("tv shows list.txt", "r")
    books = open("books list.txt", "r")
    categories = ""
    file = open("temp.txt", "a+")  # File which will contain words from chosen categories
    if "b" or "g" or "m" or "t" in choice:
        if "m" in choice:
            categories += "Movies / "
            for i in movies.readlines():
                file.write(i)
        if "g" in choice:
            categories += "Games / "
            for j in games.readlines():
                file.write(j)
        if "t" in choice:
            categories += "TV-Shows / "
            for k in tv.readlines():
                file.write(k)
        if "b" in choice:
            categories += "Books / "
            for t in books.readlines():
                file.write(t)
        categories = categories[0:-3]  # Will go in label
    movies.close()  # Close word files
    books.close()
    tv.close()
    games.close()
    file.close()

    # Get lines count
    categories_file = open("temp.txt", "r")
    count_lines = get_lines_count(categories_file)
    categories_file.close()

    # Get random word to guess
    random_num = random.randint(1, count_lines)  # Get a random integer
    word_to_guess = get_word(random_num)
    word_to_guess = word_to_guess[0:-1]  # Remove the "\n" char

    # Count word chars
    chars_count = get_chars_count(list(word_to_guess))

    # Create a variable same length as word to guess but made from _
    under_lines_guess = hide_word(word_to_guess)

    play(under_lines_guess, word_to_guess, chars_count)


def hide_word(word):
    hidden = ""
    for hide in range(len(word)):  # for 0 in (x-1)
        if word[hide] == " ":
            hidden += " "
        else:
            hidden += "_"
    return hidden


def get_chars_count(count_chars):
    counter_chars = 0
    for index in count_chars:
        if index != " ":
            counter_chars += 1
    return counter_chars


def get_lines_count(file):
    return sum(1 for line in file)  # For each line count 1+1+...


def get_word(random_number):
    global count_lines

    f = open("temp.txt", "r")
    lines = f.readlines()
    ret = lines[random_number - 1]
    f.close()
    f_new = open("temp.txt", "w")
    for line in lines:  # Write all lines to the file except the one with the word used
        if line != lines[random_number - 1]:
            f_new.write(line)
    f_new.close()

    count_lines -= 1  # Since one line is gone (used and deleted)

    return ret


def close_window():
    option_window.destroy()


def option_a():
    global count_lines
    global word_change
    global letter_change

    if word_change <= 0:
        messagebox.showwarning("Used it all", "You used all of your word change options!")
        option_window.destroy()
        return

    # Get random word to guess
    random_num = random.randint(1, count_lines)  # Get a random integer
    word_to_guess = get_word(random_num)
    word_to_guess = word_to_guess[0:-1]  # Remove the "\n" char

    # Count word chars
    chars_count = get_chars_count(list(word_to_guess))

    # Create a variable same length as word to guess but made from _
    under_lines_guess = hide_word(word_to_guess)
    word_change -= 1

    play_window.destroy()
    option_window.destroy()

    play(under_lines_guess, word_to_guess, chars_count)


def option_b():
    global chars_bank
    global counter
    global letter_change

    if letter_change <= 0:
        messagebox.showwarning("Used it all", "You used all of your letter helper options!")
        option_window.destroy()
        return

    answer_b = list(wordd)  # When done, do - "".join(list to join as string)
    upper_word = wordd.upper()
    upper_word_list_b = list(upper_word)

    len_wordd = len(wordd) - 1
    used_check = True
    while used_check:
        random_num = random.randint(0, len_wordd)
        char_reveal = wordd[random_num - 1]

        if char_reveal not in chars_bank:
            chars_bank += char_reveal
            while char_reveal.upper() in str(answer_b).upper():
                print(char_reveal.upper() + str(answer_b).upper())
                i = upper_word_list_b.index(char_reveal.upper())  # Change input char and it's duplicates
                under_lines[i] = answer_b[i]
                answer_b[i] = " "
                upper_word_list_b[i] = " "
                counter -= 1
            if counter == 0:
                messagebox.showinfo("WINNER", "You win!!!")
                answer_ = messagebox.askyesno("HangMan", "Would you like to play again?")
                if answer_ == 0:
                    quit_game()
                else:
                    new_game_window.destroy()
                    play_window.destroy()
                    option_window.destroy()
                    root.deiconify()
            used_check = False

    letter_change -= 1

    list_chars_bank_ = list(chars_bank)
    bank_lbl = Label(play_window, text="Used characters bank:\n" + " ".join(list_chars_bank_).upper())
    canvas_play.create_window(70, 270, anchor=CENTER, window=bank_lbl)

    underlines_lbl = Label(play_window, text=" ".join(under_lines))
    canvas_play.create_window(400, 310, anchor=CENTER, window=underlines_lbl)

    guesses_lbl = Label(play_window, text="You have " + str(guesses) + " guesses left")
    canvas_play.create_window(400, 340, anchor=CENTER, window=guesses_lbl)

    option_window.destroy()


def assistance():
    global word_change
    global letter_change

    global option_window

    if word_change == 0 and letter_change == 0:
        messagebox.showinfo("Assistance menu", "You don't have any more assistance options to use.")
    else:
        option_window = Toplevel()
        option_window.title("Assistance menu")
        option_window.iconbitmap("death.ico")
        option_window.geometry("270x219")
        option_window.resizable(width=False, height=False)
        option_window.attributes("-topmost", "true")

        # Create canvas and add background
        canvas_option = Canvas(option_window, width="270", height="219")
        canvas_option.pack()

        option_bg = ImageTk.PhotoImage(Image.open("choose_wise.png").resize((270, 219), Image.ANTIALIAS))
        canvas_option.background = option_bg
        canvas_option.create_image(0, 0, anchor=NW, image=option_bg)

        option_text = ("Choose an option:\nA) Change word (uses left: " + str(word_change)
                       + ")\nB) Letter helper (uses left: " + str(letter_change) + ")")

        option_lbl = Label(option_window, text=option_text, bg="bisque")
        canvas_option.create_window(135, 55, anchor=CENTER, window=option_lbl)

        option_a_btn = Button(option_window, text="Option A", borderwidth=5, command=option_a)
        canvas_option.create_window(85, 150, anchor=CENTER, window=option_a_btn)

        option_b_btn = Button(option_window, text="Option B", borderwidth=5, command=option_b)
        canvas_option.create_window(185, 150, anchor=CENTER, window=option_b_btn)

        cancel_btn = Button(option_window, text="Nah... I don't need any help", borderwidth=5,
                            command=close_window)
        canvas_option.create_window(135, 195, anchor=CENTER, window=cancel_btn)


def my_answer():
    global chars_bank

    global wordd

    global counter

    global guesses

    global list_chars_bank

    global under_lines

    if e.get()[0:1] in "\n =+-*/.`~!@#$%^&*()_,';:":
        messagebox.showwarning("Illegal input",
                               "Input is illegal. Enter a character in the range of (a-z) and (0-9)")
        e.delete(0, "end")
        return
    if e.get()[0:1] in chars_bank:
        messagebox.showwarning("Illegal input",
                               "Input was used before.")
        e.delete(0, "end")
        return
    else:
        len_align = (len(chars_bank) + 1) % 10
        if len_align == 0:
            chars_bank += "\n"
        chars_bank += e.get()[0:1]
        if e.get()[0:1].upper() in str(answer).upper():  # upper in order to ignore if the letter is written
            while e.get()[0:1].upper() in str(answer).upper():  # Check if its there more than once
                i = upper_word_list.index(e.get()[0:1].upper())  # Returns index of the letter guessed
                under_lines[i] = answer[i]
                answer[i] = " "
                upper_word_list[i] = " "
                counter -= 1
                if counter == 0:
                    messagebox.showinfo("WINNER", "You win!!!")
                    answer_ = messagebox.askyesno("HangMan", "Would you like to play again?")
                    if answer_ == 0:
                        quit_game()
                    else:
                        new_game_window.destroy()
                        play_window.destroy()
                        root.deiconify()
        else:
            guesses -= 1
            if guesses == 4:
                play_bg4 = ImageTk.PhotoImage(Image.open("hangman1.png").resize((300, 250), Image.ANTIALIAS))
                canvas_play.background = play_bg4
                canvas_play.create_image(0, 0, anchor=NW, image=play_bg4)
            if guesses == 3:
                play_bg3 = ImageTk.PhotoImage(Image.open("hangman2.png").resize((300, 250), Image.ANTIALIAS))
                canvas_play.background = play_bg3
                canvas_play.create_image(0, 0, anchor=NW, image=play_bg3)
            if guesses == 2:
                play_bg2 = ImageTk.PhotoImage(Image.open("hangman3.png").resize((300, 250), Image.ANTIALIAS))
                canvas_play.background = play_bg2
                canvas_play.create_image(0, 0, anchor=NW, image=play_bg2)
            if guesses == 1:
                play_bg1 = ImageTk.PhotoImage(Image.open("hangman4.png").resize((300, 250), Image.ANTIALIAS))
                canvas_play.background = play_bg1
                canvas_play.create_image(0, 0, anchor=NW, image=play_bg1)
            if guesses == 0:
                play_bg0 = ImageTk.PhotoImage(Image.open("hangman5.png").resize((300, 250), Image.ANTIALIAS))
                canvas_play.background = play_bg0
                canvas_play.create_image(0, 0, anchor=NW, image=play_bg0)
                messagebox.showinfo("SUCKER", "You lose!\nThe word was: " + wordd)
                answer_ = messagebox.askyesno("HangMan", "Would you like to play again?")
                if answer_ == 0:
                    quit_game()
                else:
                    word_change = 2  # if the user lost the game and wishes to play again, the assistance options (letter change and word change) don't reset, so added: word_change and letter_change
                    letter_change=1
                    new_game_window.destroy()
                    play_window.destroy()
                    root.deiconify()

    e.delete(0, "end")

    list_chars_bank = list(chars_bank)
    bank_lbl = Label(play_window, text="Used characters bank:\n" + " ".join(list_chars_bank).upper())
    canvas_play.create_window(70, 270, anchor=CENTER, window=bank_lbl)

    underlines_lbl = Label(play_window, text=" ".join(under_lines))
    canvas_play.create_window(400, 310, anchor=CENTER, window=underlines_lbl)

    guesses_lbl = Label(play_window, text="You have " + str(guesses) + " guesses left")
    canvas_play.create_window(400, 340, anchor=CENTER, window=guesses_lbl)


def play(hidden, word, count):
    new_game_window.withdraw()
    global play_bg
    global play_window
    global canvas_play

    global chars_bank
    global e

    global answer
    global upper_word_list
    global under_lines
    global wordd
    wordd = word

    global guesses
    guesses = 5

    global counter
    counter = count

    global list_chars_bank
    chars_bank = ""
    list_chars_bank = list(chars_bank)

    global word_change

    global letter_change

    play_window = Toplevel()
    play_window.title("H_NGM_N")
    play_window.iconbitmap("death.ico")
    play_window.geometry("800x400")
    play_window.resizable(width=False, height=False)

    # Create canvas and add background
    canvas_play = Canvas(play_window, width="800", height="450")
    canvas_play.pack()

    play_bg = ImageTk.PhotoImage(Image.open("graph.png").resize((800, 450), Image.ANTIALIAS))
    canvas_play.background = play_bg
    canvas_play.create_image(0, 0, anchor=NW, image=play_bg)

    under_lines = list(hidden)  # Will make it easier to change chars in string
    answer = list(word)  # When done, do - "".join(list to join as string)h
    upper_word = word.upper()
    upper_word_list = list(upper_word)
    chars_bank = ""

    letters_left_lbl = Label(play_window, text=str(counter) + " letters left to solve the word")
    canvas_play.create_window(400, 370, anchor=CENTER, window=letters_left_lbl)

    underlines_lbl = Label(play_window, text=" ".join(under_lines))
    canvas_play.create_window(400, 310, anchor=CENTER, window=underlines_lbl)

    guesses_lbl = Label(play_window, text="You have " + str(guesses) + " guesses left")
    canvas_play.create_window(400, 340, anchor=CENTER, window=guesses_lbl)

    bank_lbl = Label(play_window, text="Used characters bank:\n" + " ".join(list_chars_bank).upper())
    canvas_play.create_window(70, 270, anchor=CENTER, window=bank_lbl)

    back_menu_btn_ = Button(play_window, text="Main Menu", borderwidth=5, width=15,
                            command=lambda: [main_menu_(),
                                             play_window.destroy(),
                                             new_game_window.destroy()])
    canvas_play.create_window(70, 370, anchor=CENTER, window=back_menu_btn_)


    e = Entry(play_window, width=4, borderwidth=2)
    canvas_play.create_window(380, 250, anchor=CENTER, window=e)

    assistance_btn = Button(play_window, text="Other options", width=15, borderwidth=5, command=assistance)
    canvas_play.create_window(70, 30, anchor=SW, window=assistance_btn)

    input_answer = Button(play_window, text="Confirm", command=my_answer, borderwidth=5)
    canvas_play.create_window(430, 250, anchor=CENTER, window=input_answer)

    sound_btn = Button(play_window, text="Sound", command=play_music)
    canvas_play.create_window(770, 380, anchor=CENTER, window=sound_btn)


def score_board():
    return


def quit_game():
    root.destroy()


main_menu_()  # Start game
root.mainloop()
