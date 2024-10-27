import tkinter as tk

def create_grid(canvas, rows, cols, markers=[], goals=[], walls=[]):
    """Create a grid with the specified number of rows and columns."""
    cell_size = 50  # Size of each cell in the grid

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    # Draw the walls
    for (col, row) in walls:
        x1, y1 = col * cell_size, row * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="grey", outline="black")

    # Draw the goals
    for (col, row) in goals:
        x1, y1 = col * cell_size, row * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")

    # Draw the marker
    for (col, row) in markers:
        x1, y1 = col * cell_size, row * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")


def create_yellow_square(canvas, col, row, cell_size):
    """Draw the yellow square (marker)."""
    padding = 10  # To make the yellow square smaller than the cell
    x1 = col * cell_size + padding / 2
    y1 = row * cell_size + padding / 2
    x2 = x1 + cell_size - padding
    y2 = y1 + cell_size - padding
    # Create yellow square and assign a tag
    yellow_square = canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black", tags="yellow_square")
    # Bring it to the front of other canvas elements
    canvas.tag_raise("yellow_square")
    return yellow_square


def move_yellow_square(canvas, yellow_square, col, row, cell_size):
    """Move the yellow square to a new cell and force canvas update."""
    padding = 10  # To make the yellow square smaller than the cell
    x1 = col * cell_size + padding / 2
    y1 = row * cell_size + padding / 2
    x2 = x1 + cell_size - padding
    y2 = y1 + cell_size - padding
    # Move the yellow square
    canvas.coords(yellow_square, x1, y1, x2, y2)
    # Bring it to the front of other elements
    canvas.tag_raise("yellow_square")
    # Force a canvas update to immediately reflect changes
    canvas.update()

    
def animate_path(canvas, yellow_square, path, cell_size=50, delay=200):
    """Animate the yellow square along the found path."""
    def move_yellow_square(step):
        if step < len(path):
            col, row = path[step]
            x1 = col * cell_size + 10 / 2
            y1 = row * cell_size + 10 / 2
            x2 = x1 + cell_size - 10
            y2 = y1 + cell_size - 10
            canvas.coords(yellow_square, x1, y1, x2, y2)
            # Call this function again after a delay for the next step
            canvas.after(delay, move_yellow_square, step + 1)

    # Start the animation
    move_yellow_square(0)