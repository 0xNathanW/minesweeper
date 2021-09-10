package main

import (
	"fmt"
	"math/rand"
	"time"
)

func initGrid() [9][9]int {
	grid := [9][9]int{}
	return grid
}

func mineCoords(numMines int) map[[2]int]bool {
	coords := make(map[[2]int]bool)
	for n := 0; len(coords) < numMines; n++ {
		mine := [2]int{}
		rand.Seed((time.Now().UnixNano()) + int64(n))
		mine[0] = rand.Intn(9)
		rand.Seed((time.Now().UnixNano()) + 2*int64(n))
		mine[1] = rand.Intn(9)
		if !coords[mine] {
			coords[mine] = true
		}
	}
	fmt.Println(coords)
	return coords
}

func displayGrid(grid [9][9]int) {
	for _, row := range grid {
		fmt.Println(row)
	}
}

func main() {
	//displayGrid(initGrid())
	mineCoords(20)
}
