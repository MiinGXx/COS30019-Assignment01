import time

"""         DEPTH-FIRST SEARCH         """
def dfs(marker, goals, walls, rows, cols, canvas, cell_size):
    """Perform Depth-First Search (DFS) with visualized search tree changes."""
    stack = [(marker, [marker])]  # Stack to manage DFS
    visited = set()  # Keep track of visited nodes

    # Visualize the initial marker
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while stack:
        (current, path) = stack.pop()

        if current in visited:
            continue
        visited.add(current)

        # Highlight the current node as visited (e.g., in light gray)
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()
        time.sleep(0.2)  # Add a delay for better visualization

        # If we reached one of the goals, return the path
        if current in goals:
            return path

        # Get the possible neighbors (UP, LEFT, DOWN, RIGHT)
        neighbors = get_neighbors(current, walls, rows, cols)

        # Highlight the neighbors being expanded
        for neighbor in neighbors:
            if neighbor not in visited:
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.2)  # Add a delay for neighbor expansion visualization
                stack.append((neighbor, path + [neighbor]))

    return None  # No path found

"""         BREADTH-FIRST SEARCH         """
def bfs(marker, goals, walls, rows, cols, canvas, cell_size):
    """Perform Breadth-First Search (BFS) with visualized search tree changes."""
    queue = [(marker, [marker])]  # Queue to manage BFS
    visited = set()  # Keep track of visited nodes

    # Visualize the initial marker
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while queue:
        (current, path) = queue.pop(0)

        if current in visited:
            continue
        visited.add(current)

        # Highlight the current node as visited (e.g., in light gray)
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()
        time.sleep(0.1)  # Add a delay for better visualization

        # If we reached one of the goals, return the path
        if current in goals:
            return path

        # Get the possible neighbors (UP, LEFT, DOWN, RIGHT)
        neighbors = get_neighbors_inverted(current, walls, rows, cols)

        # Highlight the neighbors being expanded
        for neighbor in neighbors:
            if neighbor not in visited:
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.1)  # Add a delay for neighbor expansion visualization
                queue.append((neighbor, path + [neighbor]))

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

def get_neighbors_inverted(cell, walls, rows, cols):
    """Get valid neighbors of a cell (UP, LEFT, DOWN, RIGHT) that are not walls."""
    col, row = cell
    neighbors = []

    # Add neighbors in reverse order of the desired priority (UP, DOWN, LEFT, RIGHT).
    # UP
    if row > 0 and (col, row - 1) not in walls:
        neighbors.append((col, row - 1))
    # LEFT
    if col > 0 and (col - 1, row) not in walls:
        neighbors.append((col - 1, row))
    # DOWN
    if row < rows - 1 and (col, row + 1) not in walls:
        neighbors.append((col, row + 1))
    # RIGHT
    if col < cols - 1 and (col + 1, row) not in walls:
        neighbors.append((col + 1, row))

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
