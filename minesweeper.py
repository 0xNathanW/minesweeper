import numpy as np
import random


class MineSweeper:

    #   Game state.
    finished = False

    #   Number of mines on board.
    mine_count = 0

    #   Construct an array from given grid parameters.
    #   Construct the user_grid that will be shown to player.
    def __init__(self, grid_size, probability):
        self.grid = np.array([[0 for i in range(grid_size[0])] for j in range(grid_size[1])])
        self.user_grid = np.array([["█" for i in range(grid_size[0])] for j in range(grid_size[1])])
        self.rows = grid_size[1]
        self.cols = grid_size[0]
        self.p = probability

    #   Load grids with mines, temporarily are -99.
    #   Cells with mines add 1 to adjacent cells.
    #   Reformat numerical grid to grid with symbols.
    def init_game(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if random.random() < self.p:
                    self.grid[y][x] = -99
                    self.mine_count += 1
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

    #   Print user_array in current state to terminal.
    def display_user(self):
        grid_width = 6 * self.cols + 5
        print("%"*grid_width)
        print("   |  " + "  |  ".join([str(i) for i in range(1, self.cols + 1) if i < 10]) + "  | " +
              "  | ".join([str(i) for i in range(1, self.cols + 1) if i >= 10]) +
              ("  |" if self.cols>10 else ""))
        print("_"*grid_width)
        for row_num, row in enumerate(self.user_grid):
            if row_num != 0:
                print("-"*grid_width)
            if row_num < 9:
                print(str(row_num+1) + "  |  " + "  |  ".join([cell for cell in row]) + "  |")
            elif row_num >= 9:
                print(str(row_num+1) + " |  " + "  |  ".join([cell for cell in row]) + "  |")
        print("%"*grid_width)
        print("\n")

    #   Flag action, replaces cell in user_grid with "F"
    def flag(self, x, y):
        if self.user_grid[y][x] == ">":
            print("This cell has already been flagged.\n")
        elif self.user_grid[y][x] == self.grid[y][x]:
            print("This cell has already been revealed\n")
        else:
            self.user_grid[y][x] = ">"

    #   Reveal action, set cell in user_grid to equivalent cell in grid.
    #   If cell revealed twice, check if correct number of mines have been flagged
    #   and reveal all adjacent cells.
    #   If cell is "0", recursively call function on neighbouring cells also containing
    #   "0" until they are all revealed.
    def reveal(self, x, y):
        #   Case when user calls reveal on already revealed cell.
        if self.user_grid[y][x] == self.grid[y][x] and self.grid[y][x] != "0":
            flags_adj = 0
            for i in range(-1, 2):          # > loop used frequently to traverse adjacent cells.
                for j in range(-1, 2):
                    try:
                        if (y + i) >= 0 and (x + j) >= 0:
                            if i != 0 or j != 0:
                                if self.user_grid[y + i][x + j] == ">":
                                    flags_adj += 1
                    except IndexError:
                        pass
            #   Checks if num of adjacent flags is equal to that of digit in cell.
            if flags_adj == int(self.user_grid[y][x]):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        try:
                            if (y + i) >= 0 and (x + j) >= 0:
                                if i != 0 or j != 0:
                                    if self.grid[y+i][x+j] == "0":
                                        self.reveal((x+j), (y+i))
                                    elif self.grid[y+i][x+j] == "X" and self.user_grid[y+i][x+j] == ">":
                                        pass
                                    elif self.grid[y+i][x+j] == "X" and self.user_grid[y+i][x+j] != ">":
                                        self.game_lost()
                                    else:
                                        self.user_grid[y+i][x+j] = self.grid[y+i][x+j]
                        except IndexError:
                            pass
            else:
                print("Not all mines have been flagged.")

        else:
            self.user_grid[y][x] = self.grid[y][x]
            #   If cell is mine, lose game.
            if self.user_grid[y][x] == "X":
                self.game_lost()
            #   Case of cell containing "0".
            elif self.user_grid[y][x] == "0":
                adj_not_revealed = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        try:
                            if (y + i) >= 0 and (x + j) >= 0:
                                if i != 0 or j != 0:
                                    if self.user_grid[y+i][x+j] == "█":
                                        adj_not_revealed += 1
                                        self.user_grid[y+i][x+j] = self.grid[y+i][x+j]
                        except IndexError:
                            pass
                #   Checks to see if all adjacent cells already revealed, prevents infinite-recursion.
                if adj_not_revealed > 0:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            try:
                                if (y + i) >= 0 and (x + j) >= 0:
                                    if i != 0 or j != 0:
                                        if self.grid[y+i][x+j] == "0":
                                            self.reveal((x+j), (y+i))
                                        else:
                                            self.user_grid[y+i][x+j] = self.grid[y+i][x+j]
                            except IndexError:
                                pass
            else:
                pass

    def play_again(self):
        again = input("Play again? (Y/N)").upper()
        if again == "Y":
            main()
        if again == "N":
            exit()
        else:
            print("Invalid answer.")
            self.play_again()

    #   Show all mines if game lost.
    def game_lost(self):
        self.finished = True
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == "X":
                    self.user_grid[y][x] = "X"
        self.display_user()
        print("Unlucky pal.")
        self.play_again()

    #   Check for win condition after every move.
    def check_win(self):
        successful_flags = 0
        for y in range(self.rows):
            for x in range(self.cols):
                if self.user_grid[y][x] == ">" and self.grid[y][x] == "X":
                    successful_flags += 1
        if successful_flags == self.mine_count:
            self.finished = True
            print("Congrats, you won!!! You're prize is ... absolutely nothing.")
            self.play_again()

    #   Input move from user.
    def user_move(self):
        user_input = input("Next move...")
        if user_input.lower() == "quit":
            quit()
        if user_input.lower() == "reset":
            main()
        def invalid():
            print("Not a valid move, try again.")
            self.user_move()
        if user_input.count(",") != 2:
            return invalid()
        arr = user_input.split(",")
        arr = [x.strip() for x in arr]
        try:
            x, y, action = int(arr[0]) - 1, int(arr[1]) - 1, arr[2].upper()
            if x + 1 <= self.cols or y + 1 <= self.rows:
                if action == "R":
                    self.reveal(x, y)
                elif action == "F":
                    self.flag(x, y)
                else:
                    print("Invalid action.")
                    return invalid()
            else:
                print("Selected cell not on board.")
                return invalid()
        except (ValueError, IndexError):
            return invalid()

#   Retrieve grid-size and probability.
def query_difficulty():
    difficulty_to_grid_size = {"easy": ((6, 6), 0.2), "medium": ((10, 10), 0.25), "hard": ((18, 18), 0.3)}
    user_choice = input("Choose a difficulty: easy, medium, or hard...").lower()
    if user_choice in difficulty_to_grid_size.keys():
        return difficulty_to_grid_size[user_choice][0], difficulty_to_grid_size[user_choice][1]
    else:
        print("Invalid choice, please type easy, medium or hard.")
        return query_difficulty()


def main():
    grid_size, probability = query_difficulty()
    game = MineSweeper(grid_size=grid_size, probability=probability)
    game.init_game()
    game.display_user()
    while game.finished is False:
        game.user_move()
        game.display_user()
        game.check_win()


if __name__ == "__main__":

    print("""
    
    **************************************************************
    Welcome to:
    ___  ___                                                   
    |  \/  (_)                                                  
    | .  . |_ _ __   ___  _____      _____  ___ _ __   ___ _ __ 
    | |\/| | | '_ \ / _ \/ __\ \ /\ / / _ \/ _ \ '_ \ / _ \ '__|
    | |  | | | | | |  __/\__ \\ V  V /  __/  __/ |_) |  __/ |   
    \_|  |_/_|_| |_|\___||___/ \_/\_/ \___|\___| .__/ \___|_|   
                                               | |              
                                               |_|              
    
    **************************************************************
                                                                                      
    How to play:
        - Select a level of difficulty.
        - The board starts completely concealed.
        - The board is randomly scattered with hidden mines, denoted by "X".
        - Cells without mines contain a digit which shows the number of mines in adjacent cells.
        
        - You have the option to either reveal cells, or flag them if you think they are a mine.
        - Flagged cells are denoted by ">".
        
    IMPORTANT:
        - To make your move you type 3 characters separated by commas:
            1. the x coordinate (shown at top of grid).
            2. the y coordinate (shown to left of grid).
            3. Either "R" to reveal, or "F" to flag.
            
            EXAMPLE:"3,4,R" - reveals cell at coords (3 ,4).
                    "2,2,F" - flags cell at coords (2,2).        
            
        - If you believe you have flagged all adjacent mines, reveal the cell again to reveal
        other adjacent cells.
        - Cells containing 0 will automatically have adjacent cells revealed.
        
        - Type "reset" at anytime to reset the game, or "quit" to exit completely.
            
        - You lose the game if you reveal a mine.
        - You win the game by correctly flagging all mines on the board.
    
""")

    main()
