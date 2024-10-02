def create_grid(canvas, rows, cols, markers=None, goals=None, walls=None):
    """Function to create and display the grid in the Tkinter canvas."""
    cell_size = 50
    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if markers and (col, row) in markers:
                color = "red"
            elif goals and (col, row) in goals:
                color = "green"
            elif walls and (col, row) in walls:
                color = "gray"
            else:
                color = "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

def create_yellow_square(canvas, col, row):
    """Create a smaller yellow square on top of the red marker."""
    cell_size = 50
    square_size = 30  # Smaller size for the yellow square
    x1 = col * cell_size + (cell_size - square_size) / 2
    y1 = row * cell_size + (cell_size - square_size) / 2
    x2 = x1 + square_size
    y2 = y1 + square_size
    return canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black")