import tkinter as tk
import tkinter.font as font
import random
import platform
import time
import math


class Window(tk.Tk):

    #   Initialisation of main window.
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("Minesweeper")
        self._frame = None
        self.switch_frame(Menu)

    #   Method to switch between different frames.
    #   Can be called within each frame itself.
    def switch_frame(self, FrameName, **kwargs):
        if FrameName == Menu:
            next = FrameName(self)
        if FrameName == MineSweeper:
            next = FrameName(self, kwargs.get("grid_size"), kwargs.get("mines"))
        if FrameName == GameOver:
            next = FrameName(self, kwargs.get("state"), kwargs.get("time_"))
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
    - All cells completely concealed.
    - The board is randomly scattered with hidden mines, denoted by "X".
    - Cells without mines contain a digit showing the number of mines in neighbouring cells.
    
    - You can flag cells you think are mines with right click.
    - Flagged cells are denoted by "F".
    - Cells can be revealed with left click.   
    - Cells containing 0 will automatically have neighbouring cells revealed.
    
    - You lose the game if you reveal a mine.
    - You win the game by correctly flagging all mines on the board.\n
"""

    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="black", padx=20)
        tk.Frame.__init__(self, master, bg="black", padx=20)

        titleTextFont = font.Font(size=14, family="Courier", weight="bold")
        title = tk.Label(self, text=self.title, bg="black", fg="magenta", font=titleTextFont)
        title.pack()

        #   Adding instructions to frame.
        introTextFont = font.Font(size=12, family="Unispace")
        intro = tk.Label(self, text=self.intro_text, justify="left", bg="black", fg="white", font=introTextFont)
        intro.pack()

        #   Adding difficulty buttons that call main game frame with relevant difficulty parameters.
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
        self.game_state = True
        #   Reference grid in the background that we can query.
        self.ref_grid = [[0 for i in range(self.cols)] for j in range(self.rows)]
        #   Dict to track flagged cells.
        self.flag_dict = {}
        #   Dict to track which cells remain concealed.
        self.hidden_dict = {}
        self.start_time = None

        #   Random coordinates for mines, ensuring no duplicates.
        self.mine_coords = set()
        while len(self.mine_coords) < self.mines:
            self.mine_coords.add((random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)))
        for y in range(self.rows):
            for x in range(self.cols):
                if (y, x) in self.mine_coords:
                    self.ref_grid[y][x] = -1

        #   Setting numbers of other cells in reference grid based on neighbouring mine number.
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

        self.header_subframe = tk.Frame(self, bg="black")
        self.header_subframe.grid(row=0, column=0)
        self.cell_subframe = tk.Frame(self, bg="black")
        self.cell_subframe.grid(row=1, column=0)
        self.rowconfigure(1, weight=5)

        headerFont = font.Font(family="Unispace", size=12)

        #   Button to take back to menu frame.
        menu_button = tk.Button(self.header_subframe,
                                text="Menu", font=headerFont,
                                width=12, height=2,
                                fg="white", bg="black", bd=10,
                                justify="left",
                                command=lambda: master.switch_frame(Menu))
        menu_button.grid(row=0, column=0)

        timerFont = font.Font(family="Unispace", size=20)
        self.timer = tk.Label(self.header_subframe,
                         text="00:00", font= timerFont,
                         height=2, width=7,
                         justify="center",
                         fg="white", bg="black")
        self.timer.grid(row=0, column=1)

        #   Button to exit program.
        exit_button = tk.Button(self.header_subframe,
                                text="Exit", font=headerFont,
                                fg="red", bg="black", bd=10,
                                width=12, height=2,
                                justify="right",
                                command=lambda: exit())
        exit_button.grid(row=0, column=2)

        tk.Label(self.header_subframe, text="\n", bg="black").grid(row=1, columnspan=3)

        #   Cover all cells
        for y in range(self.rows):
            for x in range(self.cols):
                self.cover_cell(y, x)

        self.update_timer()

    #   Continually updates the timer every 1sec.
    def update_timer(self):
        print("checking time")
        if self.start_time is None:
            self.start_time = time.time()
        end_time = time.time()
        elapsed = math.floor(end_time - self.start_time)
        mins, secs = divmod(elapsed, 60)
        print(f"{mins:02}:{secs:02}")
        self.timer.config(text=f"{mins:02}:{secs:02}")
        if self.game_state:
            self.after(1000, self.update_timer)

    def cover_cell(self, y, x):
        #   Cover cell with black buttonl.
        #   Bind right click to flag cell.
        #   Bind left click to reveal cell.
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
            #   Sets content of cell relevent to reference grid.
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

        #   Lose the game if cell is a mine.
        if self.ref_grid[y][x] == -1:
            self.game_lost()
        #   If the cell has 0 neighbouring mines reveal all neighbours.
        #   Recursively call if neighbours also 0.
        #   Until all surrounding 0 cells have all neighbours revealed.
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

            #   Check there are still hidden neighbours to prevent infinite recursion.
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
        #   Flag cell and check if game is won.
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
        #   If cell is mine reveal all other mines.
        #   After delay switch to GameOver frame.
        self.game_state = False
        cellFont = font.Font(family="Tw Cen MT Condensed Extra Bold", weight="bold", size=10)
        for y in range(self.rows):
            for x in range(self.cols):
                if self.ref_grid[y][x] == -1:
                    mine = tk.Label(self.cell_subframe, text="X", font=cellFont,
                                    height=3, width=7, bg="red", relief="sunken")
                    mine.grid(row=y, column=x)
        self.master.after(3000, lambda: self.master.switch_frame(GameOver, state="lose", time_=self.timer.cget("text")))

    def check_game_won(self):
        #   Check if all mines are flagged and nothing else.
        #   If so game is won, reveal all cells and switch frame to GameOver after delay.
        if list(self.flag_dict.values()).count(True) == self.mines:
            correct_mines = 0
            for mine in self.mine_coords:
                if self.flag_dict[mine] is True:
                    correct_mines += 1
            if correct_mines == self.mines:
                self.game_state = False
                for coords in self.hidden_dict.keys():
                    if coords not in self.mine_coords and self.hidden_dict[coords] is True:
                        self.reveal_cell(coords[0], coords[1])
                self.master.after(3000, lambda: self.master.switch_frame(GameOver, state="win", time_=self.timer.cget("text")))


class GameOver(tk.Frame):

    def __init__(self, master, state, time_):
        tk.Frame.__init__(self, master, bg="black", padx=30, pady=30)

        msgFont = font.Font(size=28, family="Unispace")
        buttonFont = font.Font(size=26, weight="bold", family="Unispace")
        #   Different messages if game was won or lost.
        if state == "win":
            msg = tk.Label(self, text=f"Congrats you won!.\n Time completed: {time_}\nPlay again?\n", font=msgFont,
                           bg="black", fg="white", padx=50)
            msg.pack()
        elif state == "lose":
            msg = tk.Label(self, text=f"Unlucky, You lost!.\nTime: {time_}\nPlay again?\n", font=msgFont,
                           bg="black", fg="white", padx=50)
            msg.pack()
        #   Button back to menu frame.
        yes = tk.Button(self, text="Yes", font=buttonFont, bg="black", fg="green", bd=20,
                        height=1, width=10, command=lambda: master.switch_frame(Menu))
        yes.pack()
        #   Button to exit.
        no = tk.Button(self, text="No", font=buttonFont, bg="black", fg="red", bd=20,
                       height=1, width=10, command=lambda: exit())
        no.pack()


main = Window()
main.mainloop()
