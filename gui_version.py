import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import numpy as np
import random
import platform

class Window(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Minesweeper")
        self._frame = None
        self.switch_frame(Menu)

    def switch_frame(self, FrameName, *args):
        next = FrameName(self) if not args else FrameName(self, args[0], args[1])
        if self._frame is not None:
            self._frame.destroy()
        self._frame = next
        self._frame.pack()


class Menu(tk.Frame):

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

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        introTextFont = font.Font(size=12)
        intro = tk.Label(self, text=self.intro_text, justify="left")
        intro["font"] = introTextFont
        intro.pack()
        buttonFont = font.Font(size=20, weight="bold")
        levels = {"Easy": ["green", lambda: master.switch_frame(MineSweeper, (9, 9), 10)],
                  "Medium": ["blue", lambda: master.switch_frame(MineSweeper, (16, 16), 40)],
                  "Hard": ["red", lambda: master.switch_frame(MineSweeper, (30, 16), 99)],
                  "Quit": ["black", lambda: exit()]}
        for level in levels:
            button = tk.Button(self,
                            text=level,
                            width=20,
                            fg=levels[level][0],
                            command=levels[level][1])
            button["font"] = buttonFont
            button.pack()
        tk.Label(self, text="\n\n").pack()


class MineSweeper(tk.Frame):

    def __init__(self, master, grid_size, mines):
        tk.Frame.__init__(self, master)
        self.cols = grid_size[0]
        self.rows = grid_size[1]
        self.mines = mines
        tk.Label(self, text=f"Cols: {self.cols}, Rows: {self.rows}, Mines: {self.mines}.  You fuckign god.").pack()
        mine_coords = set()
        while len(mine_coords) < self.mines:
            mine_coords.add((random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)))
        print(mine_coords)

main = Window()
main.mainloop()



