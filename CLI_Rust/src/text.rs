// Text constants to build display.

pub const FLAG: &[u8] = "F".as_bytes();
pub const MINE: &[u8] = "X".as_bytes();
pub const HIDDEN: &[u8] = "#".as_bytes();
pub const SPACE: &[u8] = " ".as_bytes();

pub const TOP_LEFT: &[u8] =" ┌".as_bytes();
pub const TOP_RIGHT: &[u8] = "┐".as_bytes();
pub const BOTTOM_LEFT: &[u8] = " └".as_bytes();
pub const BOTTOM_RIGHT: &[u8] = "┘".as_bytes();
pub const VERTICAL: &[u8] = " │".as_bytes();
pub const HORIZONTAL: &[u8] = "─".as_bytes();
pub const TOP_TEE: &[u8] = "┬".as_bytes();
pub const BOTTOM_TEE: &[u8] = "┴".as_bytes();
pub const LEFT_TEE: &[u8] = "├".as_bytes();
pub const RIGHT_TEE: &[u8] = "┤".as_bytes();
pub const CROSS: &[u8] = "┼".as_bytes();

pub const MENU: &str = "
╔═══════════════════════════════╗
║           MineSweeper         ║
║                               ║
║─────┬  Select difficulty  ────║
║     │                         ║
║  1  │ Beginner                ║
║  2  │ Intermediate            ║
║  3  │ Hard                    ║
║  q  │ Quit                    ║
║     │                         ║
╚═════╧═════════════════════════╝";

