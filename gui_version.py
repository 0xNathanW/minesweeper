from tkinter import *
from tkinter import ttk
import tkinter.font as font
import numpy as np
import random

class Menu:

    intro_text = """
    **************************************************************
    Welcome to:
                            Minesweeper   
    **************************************************************
                                                                                      
    How to play:
        - Select a level of difficulty.
        - The board starts completely concealed.
        - The board is randomly scattered with hidden mines, denoted by "X".
        - Cells without mines contain a digit which shows the number of mines in adjacent cells.
        
        - You have the option to either reveal cells, or flag them if you think they are a mine.
        - Flagged cells are denoted by ">".
            
        - If you believe you have flagged all adjacent mines, reveal the cell again to reveal
        other adjacent cells.
        - Cells containing 0 will automatically have adjacent cells revealed.
        
        - Type "reset" at anytime to reset the game, or "quit" to exit completely.
            
        - You lose the game if you reveal a mine.
        - You win the game by correctly flagging all mines on the board.\n
"""

    def __init__(self, window):
        self.menu_frame = ttk.Frame(window)
        self.menu_frame.pack()

    def button_command(self, difficulty):
        difficulty_dict = {"easy": ((9, 9), 10), "medium": ((16, 16), 40), "hard": ((30, 16), 99)}
        global grid_size, number_of_mines
        grid_size, number_of_mines = difficulty_dict[difficulty][0], difficulty_dict[difficulty][1]
        self.menu_frame.destroy()
        print(difficulty_dict[difficulty])


    def develop_menu(self):
        buttonFont = font.Font(size=20, weight="bold")
        Label(self.menu_frame, text=self.intro_text, justify=LEFT).pack()
        levels = {"Easy": ["green", lambda: self.button_command("easy")],
                   "Medium": ["blue", lambda: self.button_command("medium")],
                   "Hard": ["red", lambda: self.button_command("hard")],
                   "Quit": ["black", lambda: exit()]}
        for level in levels:
            button = Button(self.menu_frame,
                                text=level,
                                width=20,
                                fg=levels[level][0],
                                justify=CENTER,
                                command=levels[level][1])
            button["font"] = buttonFont
            button.pack()
        Label(self.menu_frame, text="\n\n").pack()

    def clear_window(self):
        self.menu_frame.destroy()


class MineSweeper:

    def __init__(self, window, grid_size, number_of_mines):
        self.frame = Frame(window)
        self.frame.pack()
        self.rows = grid_size[1]
        self.cols = grid_size[0]
        self.mines = number_of_mines
        self.reference_grid = np.array([[0 for i in range(grid_size[0])] for j in range(grid_size[1])])

    def init_reference_grid(self):
        mine_coords = set()
        while len(mine_coords) < self.mines:
            mine_coords.add((random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)))
        print(mine_coords)
        for y, x in mine_coords:
            self.reference_grid[y][x] = -99
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if (y + i) >= 0 and (x + j) >= 0:
                            self.reference_grid[y + i][x + j] += 1
                    except IndexError:
                        pass
        display = np.zeros(self.reference_grid.shape, dtype="str")
        for y in range(self.rows):
            for x in range(self.cols):
                display[y][x] = "X" if self.reference_grid[y][x] < -50 else str(self.reference_grid[y][x])
        self.reference_grid = display

    def gui_setup(self):
        for x in range(self.cols):
            for y in range(self.cols):
                cell  = Button(self.frame, text=" ")
                cell.grid(column=x, row=y)





def create_window():
    window = Tk()
    window.title("MineSweeper")
    return window

grid_size = None
number_of_mines = None

window = create_window()
menu = Menu(window)
difficulty = menu.develop_menu()
game = MineSweeper(window=window, grid_size=(10,10), number_of_mines=10)


window.mainloop()



