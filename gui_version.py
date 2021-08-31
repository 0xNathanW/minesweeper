from tkinter import *
from tkinter import ttk
import tkinter.font as font

test
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
        - You win the game by correctly flagging all mines on the board.
"""

    def __init__(self, root):
        self.menu_frame = ttk.Frame(root).pack()

    def insert_menu_widgets(self):
        buttonFont = font.Font(size=20)
        Label(self.menu_frame, text=self.intro_text, justify=LEFT).pack()
        easy = Button(self.menu_frame, text="Easy", padx=50, fg="green", justify=CENTER)
        easy["font"] = buttonFont
        easy.pack()
        intermediate = Button(self.menu_frame, text="Intermediate", padx=15.5, fg="blue", justify=CENTER)
        intermediate["font"] = buttonFont
        intermediate.pack()
        hard = Button(self.menu_frame, text="Hard", padx=50, fg="red", justify=CENTER)
        hard["font"] = buttonFont
        hard.pack()
        Label(self.menu_frame, text="\n\n").pack()

def create_root():
    root = Tk()
    root.title("MineSweeper")
    return root

root = create_root()
menu = Menu(root)
menu.insert_menu_widgets()

root.mainloop()



