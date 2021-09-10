package main

import (
	"fmt"
	"math/rand"
	"time"
)

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
	return coords
}

func initReferenceGrid() [9][9]int {
	grid := [9][9]int{}
	mines := mineCoords(10)
	for k := range mines {
		grid[k[0]][k[1]] = -9
	}
	return grid
}

func displayGrid(grid [9][9]int) {
	for _, row := range grid {
		for _, cell := range row {
			fmt.Printf(" %02d ", cell)
		}
		fmt.Print("\n")
	}
}

//func getNeighbours(x , y int) []int {
//	pivot := [3]int{-1, 0, 1}
//	for i := range pivot {
//		for j := range pivot {
//
//		}
//	}
//}

func main() {
	referenceGrid := initReferenceGrid()
	displayGrid(referenceGrid)
}
