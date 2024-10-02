import tkinter as tk
from grid import create_grid, create_yellow_square, animate_path
from searchstrategy import dfs

def create_grid_window(rows, cols, marker, goals, walls, cell_size=50):
    """Create and display the Tkinter GUI window with the grid and animate the yellow square to the goal."""
    window = tk.Tk()
    window.title("Grid Visualization")

    # Create canvas for grid
    canvas = tk.Canvas(window, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    # Create and display the grid
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

    # Perform DFS search to find the path to the goal
    path = dfs(marker, goals, walls, rows, cols)
    
    if path:
        # Create the yellow square at the starting position
        yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)

        # Animate the yellow square along the found path
        animate_path(canvas, yellow_square, path)
    else:
        print("No path to the goal was found.")

    window.mainloop()
