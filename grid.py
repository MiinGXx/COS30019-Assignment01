def create_grid(canvas, rows, cols, markers, goals, walls, cell_size=50):
    """Draw the grid with walls, goals, and the marker."""
    # Draw the grid lines
    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    # Draw walls
    for (col, row) in walls:
        x1, y1 = col * cell_size, row * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="grey", outline="black")

    # Draw goals
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
    return canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black")
    
    
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
