import tkinter as tk
from grid import create_grid, create_yellow_square
from searchstrategy import dfs_search_store_moves

def create_grid_window(rows, cols, marker, goals, walls):
    """Create and display the Tkinter GUI window with grid, and allow user-controlled DFS navigation."""
    window = tk.Tk()
    window.title("Grid Visualization")

    # Create canvas for grid
    canvas = tk.Canvas(window, width=cols * 50, height=rows * 50)
    canvas.pack()

    # Create and display the grid
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

    # Create the yellow square on top of the marker cell
    yellow_square = create_yellow_square(canvas, marker[0], marker[1])

    # Retrieve the full move history using DFS
    move_history = dfs_search_store_moves(marker, goals, walls, rows, cols)

    # Index to track the current position in move_history
    move_index = [0]  # Using list to make it mutable inside functions

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

    def next_move():
        """Move the yellow square to the next position in DFS."""
        if move_index[0] < len(move_history) - 1:  # Prevent going out of bounds
            move_index[0] += 1
            new_pos, moves = move_history[move_index[0]]
            update_square(new_pos)
            print(f"Moved to {new_pos}, Moves: {moves}")

    def previous_move():
        """Move the yellow square to the previous position in DFS."""
        if move_index[0] > 0:  # Prevent going out of bounds
            move_index[0] -= 1
            new_pos, moves = move_history[move_index[0]]
            update_square(new_pos)
            print(f"Reverted to {new_pos}, Moves: {moves}")

    # Add Next and Previous buttons
    next_button = tk.Button(window, text="Next Move", command=next_move)
    next_button.pack(side=tk.LEFT, padx=10)

    prev_button = tk.Button(window, text="Previous Move", command=previous_move)
    prev_button.pack(side=tk.LEFT, padx=10)

    # Initialize the window
    window.mainloop()
