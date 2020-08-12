import pygame as pg
from play import play_game
import tkinter as tk
from threading import Thread

pg.init()

root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=400)
canvas.pack()


def launch_game():

    cellSize = 50
    screen = pg.display.set_mode((cellSize * 9, cellSize * 9))

    thickness = 40
    initial_color = (255, 255, 255, 0)

    cx = pg.Surface((200, 200), pg.SRCALPHA, 32)
    cx = cx.convert_alpha(cx)
    pg.draw.line(cx, (255, 0, 0), [0, 0], [200, 200], thickness)
    pg.draw.line(cx, (255, 0, 0), [200, 0], [0, 200], thickness)

    co = pg.Surface((200, 200), pg.SRCALPHA, 32)
    co = co.convert_alpha(co)
    pg.draw.circle(co, (0, 0, 255), [100, 100], 100, thickness)

    tie = pg.Surface((200, 200), pg.SRCALPHA, 32)
    tie = tie.convert_alpha(tie)
    pg.draw.circle(tie, (107, 3, 252), [100, 100], 100, thickness)
    pg.draw.line(tie, (107, 3, 252), [0, 0], [200, 200], thickness)
    pg.draw.line(tie, (107, 3, 252), [200, 0], [0, 200], thickness)

    play_game(screen, cpu_first.get(), autoplay.get(), entry.get(), cx, co, tie, cellSize, is_threaded.get())


def give_info():
    window = tk.Tk()
    canvas = tk.Canvas(window, width=300, height=200)
    canvas.pack()
    text = tk.Text(canvas)
    text.insert('1.0',  "RULES\n\n"
                        "Ultimate tic tac toe is tic tac toe in tic tac toe. You have a 3x3 game, each of which "
                        "is a game of 3x3 tic tac toe. The first player goes anywhere. Each subsequent play "
                        "must happen in the board that is placed in the spot of which the smaller cell was placed. "
                        "For example, if I was to place my piece in the top-right cell of a board, my opponent must "
                        "place their piece in the top-right board of the game. If the opponent sends you to a "
                        "already won / tied board, you may place your piece in any cell that isn't in a won board. "
                        "A player wins if they win 3 boards in a row like in a regular tic tac toe game. So "
                        "you must win a row, column, or diagonal of the larger game to win the game. "
                        "Smaller boards are won / tied by regular tic tac toe rules. If there is a tie in the larger "
                        "game, the person with more boards wins. \n"
                        "\nAPP HELP\n\n"
                        "\"Uses threads\": This essentially means that you will able to move and close the game screen "
                        "while the CPU is thinking. This does slow down the game though\n"
                        "\"CPU goes first\": Dictates if the computer goes first\n"
                        "\"Autoplay\": This means that 2 CPUs of the difficulty that you set will play "
                        "against each other\n"
                        "\"Difficulty\": Sets the difficulty of the CPU. Basically means how many half-moves "
                        "the bot will think ahead"
                        "\nAPP INFO\n\n"
                        "The algorithm used here is called \"minimax\"\n"
                        "I did not the invent the minimax algorithm or ultimate tic tac toe\n"
                        "This app was developed and published by Stas Gannutin")
    text.configure(state='disabled', font='Sans')
    text.pack()


button = tk.Button(root, text='Start', command=launch_game)

button.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)

is_threaded = tk.BooleanVar()
is_threaded.set(True)

check = tk.Checkbutton(root, text="Uses threads (recommended)", variable=is_threaded)
check.place(rely=0.5, relx=0, relwidth=1)

cpu_first = tk.BooleanVar()

check2 = tk.Checkbutton(root, text='CPU goes first', variable=cpu_first)
check2.place(rely=0.57, relx=0, relwidth=1)

autoplay = tk.BooleanVar()

check3 = tk.Checkbutton(root, text='Autoplay', variable=autoplay)
check3.place(rely=0.64, relx=0, relwidth=1)

label = tk.Label(text='Difficulty')
label.place(rely=0.75, relx=0, relwidth=1)

entry = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
entry.set(4)
entry.place(rely=0.8, relx=0, relwidth=1)

button1 = tk.Button(root, command=give_info, text='Info and help')
button1.place(relx=0.35, rely=0.9, relwidth=0.3, relheight=0.1)

root.mainloop()

pg.quit()


'''
cellSize = 50
screen = pg.display.set_mode((cellSize * 9, cellSize * 9))

thickness = 40
initial_color = (255, 255, 255, 0)

cx = pg.Surface((200, 200), pg.SRCALPHA, 32)
cx = cx.convert_alpha(cx)
pg.draw.line(cx, (255, 0, 0), [0, 0], [200, 200], thickness)
pg.draw.line(cx, (255, 0, 0), [200, 0], [0, 200], thickness)

co = pg.Surface((200, 200), pg.SRCALPHA, 32)
co = co.convert_alpha(co)
pg.draw.circle(co, (0, 0, 255), [100, 100], 100, thickness)

tie = pg.Surface((200, 200), pg.SRCALPHA, 32)
tie = tie.convert_alpha(tie)
pg.draw.circle(tie, (107, 3, 252), [100, 100], 100, thickness)
pg.draw.line(tie, (107, 3, 252), [0, 0], [200, 200], thickness)
pg.draw.line(tie, (107, 3, 252), [200, 0], [0, 200], thickness)

run = True
clock = pg.time.Clock()'''