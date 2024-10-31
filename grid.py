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
    """Animate the yellow square along the path and stop once the goal is reached."""
    for index, (col, row) in enumerate(path):
        x1 = col * cell_size + 10 / 2
        y1 = row * cell_size + 10 / 2
        x2 = x1 + cell_size - 10
        y2 = y1 + cell_size - 10
        canvas.coords(yellow_square, x1, y1, x2, y2)
        canvas.update()
        # Stop animation when the goal is reached
        if index == len(path) - 1:
            break  # Exit the loop if this is the last cell in the path
        canvas.after(delay)

def highlight_final_path(canvas, path, goals, cell_size=50):
    """Highlight the final path in light blue with a continuous red line across the center."""
    # Fill each cell in the path with light blue, except for goal cells which remain green
    for col, row in path:
        x1, y1 = col * cell_size, row * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        if (col, row) in goals:
            fill_color = "green"
        else:
            fill_color = "lightblue"
        canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")

    # Collect all center points of cells in the path for a continuous red line
    line_coords = []
    for col, row in path:
        center_x = (col + 0.5) * cell_size
        center_y = (row + 0.5) * cell_size
        line_coords.extend([center_x, center_y])

    # Draw a single continuous red line along the path
    canvas.create_line(line_coords, fill="red", width=2)
    canvas.update()


