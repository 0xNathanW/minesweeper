//extern crate termion;
mod text;

use core::num;

use rand::Rng;

enum CellState {
    Hidden,
    Revealed,
    Flagged,
}

struct Cell {
    state: CellState,
    mine: bool,
    adjacent_mines: u8,
}

struct Game {
    size: u8,
    num_mines: u8,
    grid: Box<[Cell]>,
    
    x: u8,
    y: u8,

}

fn get_mine_coords(size: u8, num_mines: u8) -> Vec<(u8, u8)> {
    let mut rng = rand::thread_rng();
    let mut mine_coords = Vec::new();
    while mine_coords.len() < num_mines as usize {
        let x = rng.gen_range(0..size);
        let y = rng.gen_range(0..size);
        if !mine_coords.contains(&(x, y)) {
            mine_coords.push((x, y));
        }
    }
    mine_coords
}

fn new_game(size: u8, num_mines: u8) ->&mut Game {

    let mut game = Game {
        size,
        num_mines: len(mine_coords),
        x: 0,
        y: 0,
        grid: vec![Cell {
            state: CellState::Hidden,
            mine: false,
            adjacent_mines: 0,
        }; size as usize * size as usize].into_boxed_slice(),
    };

    let mut mines_placed = 0;
    while (mines_placed < num_mines) {
        let x = rng.gen_range(0..size);
        let y = rng.gen_range(0..size);
        if !mine_coords.contains(&(x, y)) {
            
        }
    }   

} 

fn main() {

    let test = get_mine_coords(5, 5, 4);
    println!("{:#?}", test);
    
}