import tkinter as tk
from grid import create_grid, create_yellow_square
from searchstrategy import dfs

def create_grid_window(rows: int, cols: int, marker: tuple[int, int], 
                       goals: list[tuple[int, int]], 
                       walls: list[tuple[int, int]], 
                       cell_size: int = 50) -> None:
    """Create and display the Tkinter GUI window with the grid."""
    window = tk.Tk()
    window.title("Grid Visualization")

    # Create canvas for grid
    canvas = tk.Canvas(window, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    # Create and display the grid
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

    # Start the DFS animation to the goal
    dfs(marker, goals, walls, rows, cols, canvas, cell_size)

    window.mainloop()

