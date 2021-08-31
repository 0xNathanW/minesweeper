import tkinter
from tkinter import ttk


class Menu:
    def __init__(self, root):
        self.root = root

    def frame(self):
        mainframe = ttk.Frame(root, padding="10 10 12 12")




    def greet(self):
        print("Greetings!")


if __name__ == "__main__":

    root = tkinter.Tk()
    root.title("MineSweeper")
    menu = Menu(root)
    root.mainloop()