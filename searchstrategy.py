import time
import heapq

"""         DEPTH-FIRST SEARCH         """
def dfs(marker, goals, walls, rows, cols, canvas, cell_size):
    """Perform Depth-First Search (DFS) with visualized search tree changes and node tracking."""
    stack = [(marker, [marker])]  # Stack to manage DFS
    visited = set()  # Keep track of visited nodes
    node_count = 0  # To track the number of nodes created

    # Visualize the initial marker
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while stack:
        (current, path) = stack.pop()

        if current in visited:
            continue
        visited.add(current)
        node_count += 1  # Count the node

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()
        time.sleep(0.2)  # Add a delay for better visualization

        # If we reached one of the goals, return the path
        if current in goals:
            directions = convert_path_to_directions(path)
            return path, node_count, directions

        # Get the possible neighbors (UP, LEFT, DOWN, RIGHT)
        neighbors = get_neighbors(current, walls, rows, cols)

        # Highlight the neighbors being expanded
        for neighbor in neighbors:
            if neighbor not in visited:
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.2)  # Add a delay for neighbor expansion visualization
                stack.append((neighbor, path + [neighbor]))

    return None, node_count, []  # No path found



"""         BREADTH-FIRST SEARCH         """
def bfs(marker, goals, walls, rows, cols, canvas, cell_size):
    """Perform Breadth-First Search (BFS) with visualized search tree changes and node tracking."""
    queue = [(marker, [marker])]  # Queue to manage BFS
    visited = set()  # Keep track of visited nodes
    node_count = 0  # To track the number of nodes created

    # Visualize the initial marker
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while queue:
        (current, path) = queue.pop(0)

        if current in visited:
            continue
        visited.add(current)
        node_count += 1  # Count the node

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()
        time.sleep(0.1)  # Add a delay for better visualization

        # If we reached one of the goals, return the path
        if current in goals:
            directions = convert_path_to_directions(path)
            return path, node_count, directions

        # Get the possible neighbors (UP, LEFT, DOWN, RIGHT)
        neighbors = get_neighbors_inverted(current, walls, rows, cols)

        # Highlight the neighbors being expanded
        for neighbor in neighbors:
            if neighbor not in visited:
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.1)  # Add a delay for neighbor expansion visualization
                queue.append((neighbor, path + [neighbor]))

    return None, node_count, []  # No path found 


"""         GREEDY BEST-FIRST SEARCH (GBFS)         """
def gbfs(marker, goals, walls, rows, cols, canvas, cell_size):
    """Perform Greedy Best-First Search (GBFS) with visualized search tree changes and node tracking."""
    # Priority queue (heap) with (heuristic, current_position, path) tuples
    priority_queue = [(heuristic(marker, goals), marker, [marker])]
    visited = set()  # Keep track of visited nodes
    node_count = 0  # To track the number of nodes created

    # Visualize the initial marker
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)

        if current in visited:
            continue
        visited.add(current)
        node_count += 1  # Count the node

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()
        time.sleep(0.2)  # Add a delay for better visualization

        # If we reached one of the goals, return the path
        if current in goals:
            directions = convert_path_to_directions(path)
            return path, node_count, directions

        # Get the possible neighbors (UP, LEFT, DOWN, RIGHT) using get_neighbors_inverted for correct priority
        neighbors = get_neighbors_inverted(current, walls, rows, cols)

        # Highlight the neighbors being expanded
        for neighbor in neighbors:
            if neighbor not in visited:
                # Introduce tie-breaking by considering the direction priority if heuristic values are the same
                heapq.heappush(priority_queue, (heuristic(neighbor, goals), neighbor, path + [neighbor]))
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.2)  # Add a delay for neighbor expansion visualization

    return None, node_count, []  # No path found

def heuristic(cell, goals):
    """Calculate the Manhattan distance from the current cell to the closest goal."""
    col, row = cell
    return min(abs(goal[0] - col) + abs(goal[1] - row) for goal in goals)






def get_neighbors(cell, walls, rows, cols):
    """Get valid neighbors of a cell (UP, LEFT, DOWN, RIGHT) that are not walls."""
    col, row = cell
    neighbors = []

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

def convert_path_to_directions(path):
    """Convert a path of coordinates to human-readable directions (up, down, left, right)."""
    directions = []
    for i in range(1, len(path)):
        current = path[i]
        previous = path[i - 1]
        if current[0] == previous[0]:  # Same column
            if current[1] == previous[1] + 1:
                directions.append("down")
            elif current[1] == previous[1] - 1:
                directions.append("up")
        elif current[1] == previous[1]:  # Same row
            if current[0] == previous[0] + 1:
                directions.append("right")
            elif current[0] == previous[0] - 1:
                directions.append("left")
    return directions

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
