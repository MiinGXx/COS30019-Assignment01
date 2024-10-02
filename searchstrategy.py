import time

def dfs(marker, goals, walls, rows, cols):
    """Perform Depth-First Search (DFS) to find a path from marker to one of the goals."""
    stack = [(marker, [marker])]  # Stack to manage DFS
    visited = set()  # Keep track of visited nodes

    while stack:
        (current, path) = stack.pop()

        if current in visited:
            continue
        visited.add(current)

        # If we reached one of the goals, return the path
        if current in goals:
            return path

        # Get the possible neighbors (UP, LEFT, DOWN, RIGHT)
        neighbors = get_neighbors(current, walls, rows, cols)

        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None  # No path found

def get_neighbors(cell, walls, rows, cols):
    """Get valid neighbors of a cell (UP, LEFT, DOWN, RIGHT) that are not walls."""
    col, row = cell
    neighbors = []

    # Add neighbors in reverse order of the desired priority (RIGHT, DOWN, LEFT, UP).
    
    # RIGHT
    if col < cols - 1 and (col + 1, row) not in walls:
        neighbors.append((col + 1, row))
    # DOWN
    if row < rows - 1 and (col, row + 1) not in walls:
        neighbors.append((col, row + 1))
    # LEFT
    if col > 0 and (col - 1, row) not in walls:
        neighbors.append((col - 1, row))
    # UP
    if row > 0 and (col, row - 1) not in walls:
        neighbors.append((col, row - 1))

    return neighbors



def highlight_cell(canvas, position, cell_size, color):
    """Highlight the cell at the given position."""
    col, row = position
    x1, y1 = col * cell_size, row * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")


def highlight_final_path(canvas, path, cell_size):
    """Highlight the final path in light blue."""
    for position in path:
        highlight_cell(canvas, position, cell_size, "lightblue")
