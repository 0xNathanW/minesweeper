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

    title = """\n
        
      __  ____                                                       
     /  |/  (_)___  ___  ______      _____  ___  ____  ___  _____    
    / /|_/ / / __ \/ _ \/ ___/ | /| / / _ \/ _ \/ __ \/ _ \/ ___/    
   / /  / / / / / /  __(__  )| |/ |/ /  __/  __/ /_/ /  __/ /        
  /_/  /_/_/_/ /_/\___/____/ |__/|__/\___/\___/ .___/\___/_/         
                                             /_/                     
                                       
          """

    intro_text = """                       
    How to play:
    - Select a level of difficulty.
    - The board starts completely concealed.
    - The board is randomly scattered with hidden mines, denoted by "X".
    - Cells without mines contain a digit which shows the number of mines in neighbouring cells.
    
    - You have the option to either reveal cells, or flag them if you think they are a mine.
    - Flagged cells are denoted by "F".
        
    - If you believe you have flagged all neighbouring mines, reveal the cell again to reveal
      neighbouring cells.
    - Cells containing 0 will automatically have adjacent cells revealed.
    
    - You lose the game if you reveal a mine.
    - You win the game by correctly flagging all mines on the board.\n
"""

    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="black")

        titleTextFont = font.Font(size=14, family="Courier", weight="bold")
        title = tk.Label(self, text=self.title, bg="black", fg="magenta", font=titleTextFont)
        title.pack()

        introTextFont = font.Font(size=12, family="Unispace")
        intro = tk.Label(self, text=self.intro_text, justify="left", bg="black", fg="white", font=introTextFont)
        intro.pack()

        buttonFont = font.Font(size=20, weight="bold", family="Unispace")
        levels = {"Easy": ["#4aff00", lambda: master.switch_frame(MineSweeper, grid_size=(9, 9), mines=10)],
                  "Medium": ["#3c84c3", lambda: master.switch_frame(MineSweeper, grid_size=(16, 16), mines=40)],
                  "Hard": ["red", lambda: master.switch_frame(MineSweeper, grid_size=(30, 16), mines=99)],
                  "Exit": ["yellow", lambda: exit()]}
        for level in levels:
            button = tk.Button(self,
                            text=level, font=buttonFont,
                            width=20,
                            bg="black", fg=levels[level][0], bd=15,
                            activebackground="white", activeforeground="black",
                            relief="raised",
                            cursor="crosshair",
                            command=levels[level][1])

            button.pack()
        tk.Label(self, text="\n\n", bg="black").pack()


class MineSweeper(tk.Frame):

    left_click = "<Button-1>"
    right_click = "<Button-2>" if platform.system() == "Darwin" else "<Button-3>"

    def __init__(self, master, grid_size, mines):
        tk.Frame.__init__(self, master, padx=20, pady=20, bg="black")
        self.master = master
        self.cols = grid_size[0]
        self.rows = grid_size[1]
        self.mines = mines
        self.mines_found = 0
        self.ref_grid = np.array([[0 for i in range(self.cols)] for j in range(self.rows)])
        self.flag_dict = {}
        self.hidden_dict = {}
        self.num_flagged = 0

        self.mine_coords = set()
        while len(self.mine_coords) < self.mines:
            self.mine_coords.add((random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)))

        for y in range(self.rows):
            for x in range(self.cols):
                if (y, x) in self.mine_coords:
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

        self.header_subframe = tk.Frame(self, bg="black")
        self.header_subframe.grid(row=0, column=0)
        self.cell_subframe = tk.Frame(self, bg="black")
        self.cell_subframe.grid(row=1, column=0)
        self.rowconfigure(1, weight=5)

        headerFont = font.Font(family="Unispace", size=12)

        menu_button = tk.Button(self.header_subframe,
                                text="Menu", font=headerFont,
                                width=12, height=2,
                                fg="white", bg="black", bd=10,
                                justify="left",
                                command=lambda: master.switch_frame(Menu))
        menu_button.grid(row=0, column=0)

        timerFont = font.Font(family="Unispace", size=20)
        timer = tk.Label(self.header_subframe,
                         text="00.00", font= timerFont,
                         height=2, width=7,
                         justify="center",
                         fg="white", bg="black")
        timer.grid(row=0, column=1)

        exit_button = tk.Button(self.header_subframe,
                                text="Exit", font=headerFont,
                                fg="red", bg="black", bd=10,
                                width=12, height=2,
                                justify="right",
                                command=lambda: exit())
        exit_button.grid(row=0, column=2)

        tk.Label(self.header_subframe, text="\n", bg="black").grid(row=1, columnspan=3)

        for y in range(self.rows):
            for x in range(self.cols):
                self.cover_cell(y, x)

    def cover_cell(self, y, x):
        cell = tk.Button(self.cell_subframe, text=" ",
                         height=3, width=7,
                         bg="black", bd=5,
                         relief="raised", cursor="crosshair")
        cell.bind(self.left_click, lambda event, y = y, x = x: self.reveal_cell(y, x))
        cell.bind(self.right_click, lambda event, y = y, x = x: self.flag_cell(y, x))
        cell.grid(row=y, column=x)
        self.flag_dict[(y, x)] = False
        self.hidden_dict[(y, x)] = True

    def reveal_cell(self, y, x):

        def cell_config(y, x):
            cellFont = font.Font(family="Impact", weight="bold", size=10)
            colour_map = {0: None, 1: "yellow", 2: "#33cc33", 3: "red", 4: "#ff66ff",
                          5: "cyan", 6: "blue", 7: "#ff9900", 8: "white", -1: "black"}

            cell = tk.Label(self.cell_subframe,
                            text=" " if self.ref_grid[y][x] == 0 else str(self.ref_grid[y][x]), font=cellFont,
                            fg=colour_map[self.ref_grid[y][x]], bg="red" if self.ref_grid[y][x] == -1 else "#666699",
                            height=3, width=7,
                            relief="sunken", bd=5, cursor="crosshair")
            cell.grid(row=y, column=x)
            self.hidden_dict[(y, x)] = False

        if self.ref_grid[y][x] == -1:
            print("game lost")
            self.game_lost()
        elif self.ref_grid[y][x] == 0:
            adj_not_revealed = 0
            cell_config(y, x)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (y + i) >= 0 and (x + j) >= 0:
                        if i != 0 or j!= 0:
                            try:
                                if self.hidden_dict[(y+i, x+j)] is True:
                                    adj_not_revealed += 1
                                    cell_config((y+i), (x+j))
                                    self.hidden_dict[(y+i, x+j)] = False
                            except KeyError:
                                pass

            if adj_not_revealed > 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (y + i) >= 0 and (x + j) >= 0:
                            if i != 0 or j != 0:
                                try:
                                    if self.ref_grid[y + i][x + j] == 0:
                                        self.reveal_cell((y + i), (x + j))
                                except IndexError:
                                    pass
        else:
            cell_config(y, x)

    def flag_cell(self, y, x):
        cellFont = font.Font(family="Impact", weight="bold", size=8)
        flag = tk.Button(self.cell_subframe, text="F", font=cellFont,
                         height=3, width=8,
                         bg="black", fg="white",
                         cursor="crosshair")
        flag.bind(self.right_click, lambda event, y = y, x = x: self.cover_cell(y, x))
        flag.grid(row=y, column=x)
        self.flag_dict[(y, x)] = True
        self.check_game_won()

    def game_lost(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.ref_grid[y][x] == -1:
                    mine = tk.Label(self.cell_subframe, text="X", height=2, width=5, bg="red", relief="sunken")
                    mine.grid(row=y, column=x)
        print(type(self.master))
        self.master.switch_frame(GameOver, state="lose")

    def check_game_won(self):
        if list(self.flag_dict.values()).count(True) == self.mines:
            correct_mines = 0
            for mine in self.mine_coords:
                if self.flag_dict[mine] is True:
                    correct_mines += 1
            if correct_mines == self.mines:
                self.master.switch_frame(GameOver, state="win")


class GameOver(tk.Frame):

    def __init__(self, master, state):
        tk.Frame.__init__(self, master)

        msgFont = font.Font(size=24)
        if state == "win":
            msg = tk.Label(self, text="Congrats you won. Would you like to play again?")
            msg["font"] = msgFont
            msg.grid(row=0, columnspan=2)
        elif state == "lose":
            msg = tk.Label(self, text="Unlucky you lost. Would you like to play again?")
            msg["font"] = msgFont
            msg.grid(row=0, columnspan=2)
        yes = tk.Button(self, text="Yes", height=3, width=5, command=lambda: master.switch_frame(Menu))
        yes.grid(row=1, column=0)
        no = tk.Button(self, text="No", height=3, width=5, command=lambda: exit())
        no.grid(row=1, column=1)




main = Window()
main.mainloop()


#   TODO: fix gameover fram
#   TODO: loss/ win animation/delay
#   TODO: make it so cant resize window

