package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	str "strings"
	"time"
)

type Cell struct {
	mine              bool
	hidden            bool
	flagged           bool
	neighbouringMines int
}

type Board struct {
	rows     int
	cols     int
	numMines int
}

func addMines(board Board, grid map[[2]int]*Cell) {
	coords := make(map[[2]int]bool)
	for n := 0; len(coords) < board.numMines; n++ {
		mine := [2]int{}
		rand.Seed((time.Now().UnixNano()) + int64(n))
		mine[0] = rand.Intn(board.cols)
		rand.Seed((time.Now().UnixNano()) + 2*int64(n))
		mine[1] = rand.Intn(board.rows)
		if !coords[mine] {
			coords[mine] = true
		}
	}
	for coord := range coords {
		grid[coord].mine = true
	}
}

func addNums(board Board, grid map[[2]int]*Cell) {
	for coord, cell := range grid {
		if !cell.mine {
			var adjMines int
			neighbours := getNeighbours(coord, board)
			for n := range neighbours {
				if grid[neighbours[n]].mine {
					adjMines++
				}
			}
			cell.neighbouringMines = adjMines
		}
	}
}

func initGrid(board Board) map[[2]int]*Cell {
	grid := make(map[[2]int]*Cell)
	for x := 0; x < board.cols; x++ {
		for y := 0; y < board.rows; y++ {
			coords := [2]int{x, y}
			grid[coords] = &Cell{
				mine:              false,
				hidden:            true,
				flagged:           false,
				neighbouringMines: 0,
			}
		}
	}
	addMines(board, grid)
	addNums(board, grid)
	return grid
}

func displayGrid(board Board, grid map[[2]int]*Cell) {
	for y := 0; y < board.rows; y++ {
		for x := 0; x < board.cols; x++ {
			coord := [2]int{x, y}
			cell := *grid[coord]
			if cell.flagged {
				fmt.Print(" F ")
			} else if cell.hidden {
				fmt.Print(" # ")
			} else if !cell.hidden && cell.mine {
				fmt.Print(" X ")
			} else {
				fmt.Printf(" %v ", cell.neighbouringMines)
			}
		}
		fmt.Print("\n")
	}
}

func getNeighbours(coord [2]int, board Board) [][2]int {
	x := coord[0]
	y := coord[1]
	var neighbours [][2]int
	pivot := [3]int{-1, 0, 1}
	for i := range pivot {
		for j := range pivot {
			if (x+pivot[i] >= 0 && y+pivot[j] >= 0) &&
				(x+pivot[i] < board.cols && y+pivot[j] < board.rows) &&
				(pivot[i] != 0 || pivot[j] != 0) {
				coord := [2]int{x + pivot[i], y + pivot[j]}
				neighbours = append(neighbours, coord)

			}
		}
	}
	return neighbours
}

func getMove(board Board) ([2]int, string) {
	var move string
	fmt.Println("Enter your move: ")
	_, err := fmt.Scanln(&move)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	if str.Count(move, ",") == 2 {
		arr := str.Split(move, ",")
		fmt.Println(arr)
		x, errX := strconv.Atoi(arr[0])
		y, errY := strconv.Atoi(arr[1])
		action := arr[2]
		if (errX == nil) && (errY == nil) &&
			(x >= 0) && (y >= 0) &&
			(x <= board.cols) && (y <= board.rows) &&
			(action == "r" || action == "f") {
			coords := [2]int{x, y}
			return coords, action
		}
	}
	fmt.Println("Invalid move.")
	return getMove(board)
}

func flag(coords [2]int, grid map[[2]int]*Cell) {
	cell := grid[coords]
	if cell.flagged {
		cell.flagged = false
	} else {
		cell.flagged = true
		fmt.Println(cell)
	}
}

func reveal(coords [2]int, grid map[[2]int]*Cell, board Board) {
	cell := grid[coords]
	if cell.mine {
		gameLost(grid, board)
	} else if !cell.hidden {
		fmt.Println("Cell already revealed")
	} else if cell.neighbouringMines == 0 {
		cell.hidden = false
		neighbours := getNeighbours(coords, board)
		hiddenAdj := 0
		for n := range neighbours {
			nCell := grid[neighbours[n]]
			if nCell.hidden {
				hiddenAdj ++
			}
		}
		if hiddenAdj > 0 {
			for n := range neighbours {
				reveal(neighbours[n], grid, board)
			}
		}
	} else {
		cell.hidden = false
	}
}

func gameLost(grid map[[2]int]*Cell, board Board) {
	for c := range grid {
		cell := grid[c]
		if cell.mine {
			cell.hidden = false
		}
	}
	fmt.Println("Unlucky you Lost :(")
	displayGrid(board, grid)
	time.Sleep(3000)
	playAgain()
}

func checkGameWon(grid map[[2]int]*Cell, board Board) {
	var flaggedMines int
	for c := range grid {
		cell := grid[c]
		if cell.mine && cell.flagged {
			flaggedMines ++
		}
	}
	if flaggedMines == board.numMines {
		fmt.Println("Congrats, you Won!! :)")
		playAgain()
	}
}

func playAgain() {
	fmt.Println("Play Again? (y/n)")
	var ans string
	_, err := fmt.Scanln(&ans)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	switch ans {
	case "y":
		main()
	case "n":
		os.Exit(0)
	default:
		fmt.Println("Invalid answer.")
		playAgain()
	}
}

func main() {
	board := Board{
		rows:     9,
		cols:     9,
		numMines: 10,
	}
	grid := initGrid(board)
	for {
		displayGrid(board, grid)
		coords, move := getMove(board)
		if move == "f" {
			flag(coords, grid)
		}
		if move == "r" {
			reveal(coords, grid, board)
		}
	}

}
