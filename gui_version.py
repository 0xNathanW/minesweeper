import tkinter as tk
import tkinter.font as font
import random
import platform
import numpy as np

class Window(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Minesweeper")
        self._frame = None
        self.switch_frame(Menu)

    def switch_frame(self, FrameName, **kwargs):
        if FrameName == Menu:
            next = FrameName(self)
        if FrameName == MineSweeper:
            next = FrameName(self, kwargs.get("grid_size"), kwargs.get("mines"))
        if FrameName == GameOver:
            next = FrameName(self, kwargs.get("state"))

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
        levels = {"Easy": ["green", lambda: master.switch_frame(MineSweeper, grid_size=(9, 9), mines=10)],
                  "Medium": ["blue", lambda: master.switch_frame(MineSweeper, grid_size=(16, 16), mines=40)],
                  "Hard": ["red", lambda: master.switch_frame(MineSweeper, grid_size=(30, 16), mines=99)],
                  "Exit": ["black", lambda: exit()]}
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

    left_click = "<Button-1>"
    right_click = "<Button-2>" if platform.system() == "Darwin" else "<Button-3>"

    def __init__(self, master, grid_size, mines):
        tk.Frame.__init__(self, master, padx=30, pady=30, bg="white")
        self.master = master
        self.cols = grid_size[0]
        self.rows = grid_size[1]
        self.mines = mines
        self.mines_found = 0
        self.ref_grid = np.array([[0 for i in range(self.cols)] for j in range(self.rows)])
        self.flag_dict = {}

        mine_coords = set()
        while len(mine_coords) < self.mines:
            mine_coords.add((random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)))
        print(mine_coords)

        for y in range(self.rows):
            for x in range(self.cols):

                self.flag_dict[(y, x)] = False

                if (y, x) in mine_coords:
                    self.ref_grid[y][x] = -1

        for y in range(self.rows):
            for x in range(self.cols):
                neighbouring_mines = 0
                if self.ref_grid[y][x] != -1:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            try:
                                if (y + i) >= 0 and (x + j) >= 0:
                                    if i != 0 or j != 0:
                                        if self.ref_grid[y + i][x + j] == -1:
                                            neighbouring_mines += 1
                            except IndexError:
                                pass
                    self.ref_grid[y][x] = neighbouring_mines
        print(self.ref_grid)

        self.menu_subframe = tk.Frame(self)
        self.menu_subframe.grid(row=0, column=0)
        self.cell_subframe = tk.Frame(self)
        self.cell_subframe.grid(row=1, column=0)
        self.rowconfigure(1, weight=5)

        menu_button = tk.Button(self.menu_subframe,
                                text="Menu",
                                fg="blue",
                                width=10,
                                height=2,
                                justify="left",
                                command=lambda: master.switch_frame(Menu))
        menu_button.grid(row=0, columnspan=5, sticky="w")

        exit_button = tk.Button(self.menu_subframe,
                                text="Exit",
                                fg="red",
                                width=10,
                                height=2,
                                justify="right",
                                command=lambda: exit())
        exit_button.grid(row=0, column = self.cols)

        for y in range(self.rows):
            for x in range(self.cols):
                cell = tk.Button(self.cell_subframe, text=" ", height=2, width=5)
                cell.bind(self.left_click, lambda event, y = y, x = x: self.reveal(y, x))
                cell.bind(self.right_click, lambda event, y = y, x = x: self.flag(y, x))
                cell.grid(row=y, column=x)

    def reveal(self, y, x):
        print(f"Reveal at {y} {x}")
        if self.ref_grid[y][x] == -1:
            print("game lost")
            self.game_lost()
        #   call game won
        else:
            cell = tk.Label(self.cell_subframe, text=str(self.ref_grid[y][x]), height=2, width=5)
            cell.grid(row=y, column=x)


    def flag(self, y, x):
        if self.flag_dict[(y, x)]:
            print(y, x, "already flagged")
            cell = tk.Button(self.cell_subframe, text=" ", height=2, width=5)
            cell.bind(self.left_click, lambda event, y=y, x=x: self.reveal(y, x))
            cell.bind(self.right_click, lambda event, y=y, x=x: self.flag(y, x))
            cell.grid(row=y, column=x)

        else:
            flag = tk.Label(self.cell_subframe, text=">", height=2, width=5)
            flag.grid(row=y, column=x)
            self.flag_dict[(y, x)] = True
            print(y, x, "flagged")


    def game_lost(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.ref_grid[y][x] == -1:
                    mine = tk.Label(self.cell_subframe, text="X", height=2, width=5, bg="red", relief="sunken")
                    mine.grid(row=y, column=x)
        print(type(self.master))
        self.master.switch_frame(GameOver, state="lose")

    def game_won(self):
        pass


class GameOver(tk.Frame):

    def __init__(self, master, state):
        tk.Frame.__init__(self, master)
        if state == "win":
            msg = tk.Label(self, text="Congrats you won. Would you like to play again?", height=4, width=10)
            msg.pack()
        elif state == "lose":
            msg = tk.Label(self, text="Unlucky you lost. Would you like to play again?", height=4, width=10)
            msg.pack()
        yes = tk.Button(self, text="Yes", height=3, width=5, command=lambda: master.switch_frame(Menu))
        yes.pack()
        no = tk.Button(self, text="No", height=3, width=5, command=lambda: exit())
        no.pack()




main = Window()
main.mainloop()



