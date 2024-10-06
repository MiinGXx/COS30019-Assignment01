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
        time.sleep(0.1)  # Add a delay for better visualization

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
                time.sleep(0.1)  # Add a delay for neighbor expansion visualization
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
# Heuristic function (Manhattan distance)
def manhattan_distance(node, goal):
    """Calculate the Manhattan distance from the current node to the goal."""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# Greedy Best-First Search (GBFS)
def gbfs(marker, goals, walls, rows, cols, canvas, cell_size):
    """Greedy Best-First Search implementation with visualization."""
    open_list = []
    heapq.heappush(open_list, (0, marker))  # priority queue with heuristic values
    came_from = {marker: None}
    visited = set()
    visited.add(marker)
    node_count = 0
    directions = []

    # Visualize the initial marker
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()
    time.sleep(0.5)  # Initial delay for better visibility

    while open_list:
        _, current = heapq.heappop(open_list)
        node_count += 1

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()
        time.sleep(0.1)  # Delay for animation effect

        if current in goals:
            # Backtrack to find the path
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()

            # Convert path to directions (up, left, down, right)
            directions = []
            for i in range(1, len(path)):
                x1, y1 = path[i - 1]
                x2, y2 = path[i]
                if x2 == x1 and y2 == y1 - 1:
                    directions.append("up")
                elif x2 == x1 and y2 == y1 + 1:
                    directions.append("down")
                elif x2 == x1 - 1 and y2 == y1:
                    directions.append("left")
                elif x2 == x1 + 1 and y2 == y1:
                    directions.append("right")

            # Highlight the final path in blue
            highlight_final_path(canvas, path, cell_size)
            return path, node_count, directions

        # Explore neighbors (prioritize based on heuristic)
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                heapq.heappush(open_list, (manhattan_distance(neighbor, goals[0]), neighbor))
                came_from[neighbor] = current
                
                # Highlight the neighbors being considered
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.1)  # Delay for neighbor visualization

    # If no path was found
    print("No path to the goal was found.")
    return None, node_count, directions  # No path found

# Helper function to get neighbors
def get_neighbors(node, walls, rows, cols):
    """Get valid neighbors of a node, excluding walls and out-of-bound cells."""
    neighbors = []
    x, y = node
    possible_moves = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]  # up, down, left, right

    for nx, ny in possible_moves:
        if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in walls:
            neighbors.append((nx, ny))

    return neighbors




"""         A* SEARCH         """
def a_star(marker, goals, walls, rows, cols, canvas, cell_size):
    """A* search algorithm implementation with visualized visited nodes."""
    open_list = []  # Priority queue for nodes to be evaluated
    heapq.heappush(open_list, (0, marker))  # Push the starting marker with a priority of 0
    came_from = {}  # To track the path
    g_score = {marker: 0}  # Cost from start to current node
    f_score = {marker: manhattan_distance(marker, goals[0])}  # Estimated total cost from start to goal
    visited = set()  # Keep track of visited nodes
    node_count = 0  # To track the number of nodes created
    directions = []  # To store directions for the final path

    while open_list:
        # Get the node with the lowest f_score
        current = heapq.heappop(open_list)[1]
        node_count += 1

        # Highlight the current node as visited (in light gray)
        highlight_cell(canvas, current, cell_size, "lightgray")  # Mark current node as visited
        canvas.update()  # Update the canvas for animation
        time.sleep(0.1)  # Add a delay for better visualization

        # Check if the current node is a goal
        if current in goals:
            # Backtrack to find the path
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            path.reverse()  # Reverse the path to get it from start to goal

            # Convert path to directions (up, left, down, right)
            directions = []
            for i in range(1, len(path)):
                x1, y1 = path[i - 1]
                x2, y2 = path[i]
                if x2 == x1 and y2 == y1 - 1:
                    directions.append("up")
                elif x2 == x1 and y2 == y1 + 1:
                    directions.append("down")
                elif x2 == x1 - 1 and y2 == y1:
                    directions.append("left")
                elif x2 == x1 + 1 and y2 == y1:
                    directions.append("right")

            return path, node_count, directions  # Return the found path

        # Explore neighbors
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1  # Assume cost to neighbor is 1

            # If the neighbor is not visited or found a better path
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current  # Record the best path to the neighbor
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goals[0])

                # If the neighbor is not already in the open list, add it
                if neighbor not in visited:
                    visited.add(neighbor)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

                # Highlight the neighbor for visualization
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")  # Optional: visualize neighbors
                canvas.update()  # Update the canvas for animation
                time.sleep(0.1)  # Add a delay for better visualization

    print("No path to the goal was found.")
    return None, node_count, directions  # No path found



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
