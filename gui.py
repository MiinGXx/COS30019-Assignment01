import tkinter as tk
from grid import create_grid, create_yellow_square
from searchstrategy import dfs_search

def create_grid_window(rows, cols, marker, goals, walls):
    """Create and display the Tkinter GUI window with the grid."""
    window = tk.Tk()
    window.title("Grid Visualization")

    # Create canvas for grid
    canvas = tk.Canvas(window, width=cols * 50, height=rows * 50)
    canvas.pack()

    # Create and display the grid
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

    # Create the yellow square on top of the marker cell
    yellow_square = create_yellow_square(canvas, marker[0], marker[1])

    # Start DFS to navigate to a goal
    moves = dfs_search(marker, goals, walls, rows, cols)
    if moves:
        print("Moves to goal:", moves)

    window.mainloop()
