import numpy as np
import random


class MineSweeper:

    #   Probability of a square being a bomb.
    p = 0.15
    #   Game state.
    finished = False

    #   Construct an array from given grid parameters.
    #   Construct grid that will be shown to player.
    def __init__(self, grid_size):
        self.grid = np.array([[0 for i in range(grid_size[0])] for j in range(grid_size[1])])
        self.user_grid = np.array([["#" for i in range(grid_size[0])] for j in range(grid_size[1])])
        self.rows = grid_size[1]
        self.cols = grid_size[0]

    #   Initialise the grid with bombs denoted by -99.
    #   Calculate number of bombs in non-bomb cells' perimeters.
    #   Reformat array to strings.
    def init_game(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if random.random() < self.p:
                    self.grid[y][x] = -99
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            try:
                                if (y+i) >= 0 and (x+j) >= 0:
                                    self.grid[y+i][x+j] += 1
                            except IndexError:
                                pass
        display = np.zeros(self.grid.shape, dtype="str")
        for y in range(self.rows):
            for x in range(self.cols):
                display[y][x] = "X" if self.grid[y][x] < -50 else str(self.grid[y][x])
        self.grid = display
        #print(self.grid)

    def display_user(self):
        print("\t\t" + "\t\t".join([str(i) for i in range(1, self.cols + 1)]))
        print("-"*((8*self.cols)+3))
        for row_num, row in enumerate(self.user_grid):
            if row_num != 0:
                print(" \t|")
            print(str(row_num+1) + "\t|\t" + "\t\t".join([cell for cell in row]))

    def flag(self, x, y):
        self.user_grid[y][x] = "F"
    #TODO Handle for flagging cells already with flags

    def reveal(self, x, y):
        self.user_grid[y][x] = self.grid[y][x]
        if self.user_grid[y][x] == "X":
            pass
        elif self.user_grid[y][x] == "0":
            print(f"{x}, {y} is 0")
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if (y + i) >= 0 and (x + j) >= 0:
                            self.user_grid[y+i][x+j] = self.grid[y+i][x+j]
                            if i != 0 or j != 0:
                                print(self.grid[y+i][x+j])
                                if self.grid[y+i][x+j] == "0" and self.user_grid[y+i][x+j] == "#":
                                    print(f"({y+i}, {x+j}) also 0")
                                    print(self.user_grid)
                                    self.reveal((y+i),(x+j))
                        else:
                            print("Conditions not met")
                    except IndexError:
                        pass
        else:
            pass



    def user_move(self):
        #   F for flag, R for reveal.
        valid_actions = ["F", "R"]
        valid = True
        user_input = input("Next move: ")
        arr = [char for char in user_input]
        if len(arr) != 3 or arr[2].upper() not in valid_actions:
            valid = False
        try:
            x, y, action = int(arr[0]) - 1, int(arr[1]) - 1, arr[2].upper()
            if x > self.cols or y > self.rows:
                valid = False
        except ValueError:
            valid = False
        if valid:
            print("valid move")
            print(f"At ({x}, {y}): {self.grid[y][x]}")
            self.user_move()

        else:
            print("Not a valid move. Try again.")
            self.user_move()


def query_difficulty():
    difficulty_to_grid_size = {"easy": (5, 5), "medium": (10, 8), "hard": (18, 14)}
    user_choice = input("Choose a difficulty: easy, medium, or hard...").lower()
    if user_choice in difficulty_to_grid_size.keys():
        return difficulty_to_grid_size[user_choice]
    else:
        print("Invalid choice, please type easy, medium or hard.")
        query_difficulty()


def main():
    #grid_size = query_difficulty()
    game = MineSweeper((5, 5))
    game.init_game()
    #game.display_user()
    # while game.finished is False:
    #     game.user_move()
    print(game.grid)
    game.reveal(1, 1)
    game.display_user()


if __name__ == "__main__":

    main()

#TODO Show all mines when game lost