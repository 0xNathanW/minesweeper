extern crate termion;
mod text;

use rand::Rng;
use termion::raw::{IntoRawMode, RawTerminal};
use termion::{clear, color, cursor, style};
use termion::input::{Keys, TermRead};
use std::char;
use std::fmt::write;
use std::io::{stdin, Stdin, Read, Write, stdout, Stdout};


#[derive(Clone, Copy)]
struct Cell {
    hidden: bool,
    flagged: bool,
    mine: bool,
    adjacent_mines: u16,
}

struct Game {
    // Game state.
    width: u16,
    total_cells: usize,
    num_mines: u16,
    grid: Box<[Cell]>,
    // Cursor position.
    x: u16,
    y: u16,
    // Input/output.
    key_stream: Keys<Stdin>,
    display: RawTerminal<Stdout>,
}

fn new_game(width: u16, num_mines: u16) -> Game {

    let input = stdin().keys();
    let output = stdout().into_raw_mode().unwrap();

    let total_cells = width as usize * width as usize;
    let mut game = Game {
        width,
        total_cells,
        num_mines,
        grid: vec![Cell {
            hidden: true,
            flagged: false,
            mine: false,
            adjacent_mines: 0,
        }; total_cells].into_boxed_slice(),

        x: 0,
        y: 0,
        
        key_stream: input,
        display: output,
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
                    let idx = game.coords_to_idx(x as u16, y as u16);
                    if game.grid[idx].mine {
                        adjacent_mines += 1;
                    }
                }
            }
            game.grid[idx].adjacent_mines = adjacent_mines;
        }
    }
    game
} 

impl Game {

    /// Returns index of cell given grid coordinates.
    fn coords_to_idx(&self, x: u16, y: u16) -> usize {
        (y * self.width + x) as usize
    }

    /// Retrieves cell at given coordinates.
    fn get_cell(&self, x: u16, y: u16) -> Cell {
        self.grid[self.coords_to_idx(x, y)]
    }

    /// Retrieve mutable cell given grid coordinates.
    fn get_mut_cell(&mut self, x: u16, y: u16) -> &mut Cell {
        &mut self.grid[self.coords_to_idx(x, y)]
    }

    fn coords_to_term(&self) -> (u16, u16) {
        let cursor_x = 4;
        let cursor_y = 2;
        (cursor_x+(self.x*2), cursor_y+self.y)
    }

    fn cursor_up(&mut self) {
        if self.y == 0 {
            self.y = self.width - 1;
        } else {
            self.y -= 1;
        }
    }

    fn cursor_down(&mut self) {
        if self.y == self.width - 1 {
            self.y = 0;
        } else {
            self.y += 1;
        }
    } 

    fn cursor_right(&mut self) {
        if self.x == self.width - 1 {
            self.x = 0;
        } else {
            self.x += 1;
        }
    }

    fn cursor_left(&mut self) {
        if self.x == 0 {
            self.x = self.width - 1;
        } else {
            self.x -= 1;
        }
    }

    /// Draw game board, all cells hidden.
    fn init(&mut self) {
        write!(self.display, "{}{}", clear::All, cursor::Goto(1, 1)).unwrap();
        // Top.
        self.display.write(text::TOP_LEFT).unwrap();
        for _ in 0..self.width {
            self.display.write(text::HORIZONTAL).unwrap();
            self.display.write(text::HORIZONTAL).unwrap();
        }
        self.display.write(text::HORIZONTAL).unwrap();
        self.display.write(text::TOP_RIGHT).unwrap();
        self.display.write(b"\n\r").unwrap();
        // Middle.
        for x in 0..self.width {
            self.display.write(text::VERTICAL).unwrap();
            for y in 0..self.width {
                self.display.write(text::SPACE).unwrap();
                self.display.write(text::HIDDEN).unwrap();
                //self.display.write(&[b'0'+self.get_cell(x, y).adjacent_mines as u8]).unwrap();
            }
            self.display.write(text::VERTICAL).unwrap();
            self.display.write(b"\n\r").unwrap();
        }
        // Bottom.
        self.display.write(text::BOTTOM_LEFT).unwrap();
        for _ in 0..self.width {
            self.display.write(text::HORIZONTAL).unwrap();
            self.display.write(text::HORIZONTAL).unwrap();
        }
        self.display.write(text::HORIZONTAL).unwrap();
        self.display.write(text::BOTTOM_RIGHT).unwrap();
        self.display.flush().unwrap();
    }

    fn game_over() {

    }

    fn neighbours(&mut self, x: u16, y: u16) -> Vec<(u16, u16)> {
        let mut neighbours = Vec::new();
        for i  in x as i16 - 1..x as i16 + 2 {
            for j  in y as i16 - 1..y as i16 + 2 {
                if i < 0 || j < 0 || i >= self.width as i16 || j >= self.width as i16 {
                    continue;
                } else if neighbours.contains(&(i as u16, j as u16)){
                    continue;
                }
                neighbours.push((i as u16, j as u16));
            }
        }
        print!("{:?}",neighbours);
        neighbours
    }

    fn reveal_cell(&mut self, x: u16, y: u16) {
        self.get_mut_cell(x, y).hidden = false;
        let (cursor_x, cursor_y) = self.coords_to_term();
        write!(self.display, "{}", cursor::Goto(cursor_x, cursor_y)).unwrap();
        if self.get_cell(x, y).adjacent_mines == 0 {
            self.display.write(text::SPACE).unwrap();
            for (x, y) in self.neighbours(x, y).into_iter() {
                if self.get_cell(x, y).hidden && !  self.get_cell(x, y).mine {
                    self.reveal_cell(x, y)
                }
            }
        } else {
            self.display.write(&[b'0'+self.get_cell(x, y).adjacent_mines as u8]).unwrap();
        }
    }


    fn run(&mut self) {
        loop {
            let key = self.key_stream.next().unwrap().unwrap();
            use termion::event::Key::*;
            
            match key {
                Up | Char('w') => self.cursor_up(),
                Down | Char('d') => self.cursor_down(),
                Right | Char('s') => self.cursor_right(),
                Left | Char('a') => self.cursor_left(),

                Char(' ') => {
                    let cell = self.get_cell(self.x, self.y);
                    if cell.mine {
                        return
                    }
                    self.reveal_cell(self.x, self.y);
                },

                Char('f') => {
                    let mut cell = self.get_mut_cell(self.x, self.y);
                    if cell.hidden && !cell.flagged {
                        cell.flagged = true;
                        self.display.write(text::FLAG).unwrap();
                    } else if cell.hidden && cell.flagged {
                        cell.flagged = false;
                        self.display.write(text::HIDDEN).unwrap();
                    }  
                },

                Char('q') => return, // Quit.

                _ => {},
            }
            let (cursor_x, cursor_y) = self.coords_to_term();
            write!(self.display, "{}", cursor::Goto(cursor_x, cursor_y)).unwrap();
            self.display.flush().unwrap();
        }
    }

}

fn main() {
    
    let mut g = new_game(10, 10);
    g.init();
    g.run()
}