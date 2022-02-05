extern crate termion;
mod text;

use rand::Rng;
use termion::event::Key;
use termion::{clear, color, cursor, style};
use termion::input::{Keys, TermRead};
use std::char;
use std::io::{stdin, Read, StdinLock, Stdin};

#[derive(Clone, Copy)]
enum CellState {
    Hidden,
    Revealed,
    Flagged,
}

#[derive(Clone, Copy)]
struct Cell {
    state: CellState,
    mine: bool,
    adjacent_mines: u8,
}

struct Game {
    // Game state.
    width: u8,
    total_cells: usize,
    num_mines: u8,
    grid: Box<[Cell]>,
    // Cursor position.
    x: u8,
    y: u8,
    // Input/output.
    key_stream: Keys<Stdin>,
}

fn new_game(width: u8, num_mines: u8) -> Game {

    let input = stdin().keys();

    let total_cells = width as usize * width as usize;
    let mut game = Game {
        width,
        total_cells,
        num_mines,
        grid: vec![Cell {
            state: CellState::Hidden,
            mine: false,
            adjacent_mines: 0,
        }; total_cells].into_boxed_slice(),

        x: 0,
        y: 0,
        
        key_stream: input,
    };

    // Place mines.
    let mut mines_placed = 0;
    let mut rng = rand::thread_rng();
    while mines_placed < num_mines {
        let idx = rng.gen_range(0..total_cells);
        if game.grid[idx].mine {
            continue;
        } else {
            game.grid[idx].mine = true;
            mines_placed += 1;
        }
    }

    // Calculate adjacent mines for each cell.
    for i in 0..width {
        for j in 0..width {
            let idx = game.coords_to_idx(i, j);
            if game.grid[idx].mine {
                continue;
            }
            let mut adjacent_mines = 0;
            // Cast as i16 to avoid overflow.
            for x  in i as i16 - 1..i as i16 + 2 {
                for y  in j as i16 - 1..j as i16 + 2 {
                    if x < 0 || y < 0 || x >= width as i16 || y >= width as i16 {
                        continue;
                    }
                    let idx = game.coords_to_idx(x as u8, y as u8);
                    if game.grid[idx].mine {
                        adjacent_mines += 1;
                    }
                }
            }
            game.grid[idx].adjacent_mines = adjacent_mines;
        }
    }
    game.print_debug();
    game
} 

impl Game {

    /// Returns index of cell given grid coordinates.
    fn coords_to_idx(&self, x: u8, y: u8) -> usize {
        (y * self.width + x) as usize
    }

    fn print_debug(&self) {
        let total = self.width as usize * self.width as usize;
        for i in 0..total {
            if self.grid[i].mine {
                print!(" X ");
            } else {
                print!(" {} ", self.grid[i].adjacent_mines);
            }
            if i % self.width as usize == self.width as usize - 1 {
                println!("");
            }
        }
    }

    /// Retrieves cell at given coordinates.
    fn get_cell(&self, x: u8, y: u8) -> Cell {
        self.grid[self.coords_to_idx(x, y)]
    }

    /// Retrieve mutable cell given grid coordinates.
    fn get_mut_cell(&mut self, x: u8, y: u8) -> &mut Cell {
        &mut self.grid[self.coords_to_idx(x, y)]
    }

    fn cursor_up(&mut self) {
        if self.y == 0 {
            self.y = self.width - 1;
        } else {
            self.y -= 1;
        }
    }

    fn cursor_down(&mut self) {
        if self.y == self.width {
            self.y = 0;
        } else {
            self.y += 1;
        }
    } 

    fn run(&mut self) {
        loop {
            let key = self.key_stream.next().unwrap().unwrap();
            use termion::event::Key::*;
            
            match key {
                Up | Char('w') => self.cursor_up(),
                Down | Char('d') => self.cursor_down(),



            }
            
        }
    }

}

fn main() {
    
    let mut g = new_game(10, 10);
    g.run()
}