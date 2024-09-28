import tkinter as tk
from grid import create_grid, create_yellow_square
from searchstrategy import dfs_search_visual

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

    def update_square(new_pos):
        """Update the yellow square's position visually on the canvas."""
        cell_size = 50
        square_size = 30  # Smaller size for the yellow square
        x1 = new_pos[0] * cell_size + (cell_size - square_size) / 2
        y1 = new_pos[1] * cell_size + (cell_size - square_size) / 2
        x2 = x1 + square_size
        y2 = y1 + square_size
        # Move the yellow square to the new position
        canvas.coords(yellow_square, x1, y1, x2, y2)
        window.update()  # Update the canvas to reflect the changes

    # Start DFS with visual updates to navigate to a goal
    moves = dfs_search_visual(marker, goals, walls, rows, cols, update_square)
    if moves:
        print("Moves to goal:", moves)

    window.mainloop()
