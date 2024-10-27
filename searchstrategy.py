import time
import heapq
from grid import create_yellow_square, move_yellow_square, animate_path
from search_tree import render_search_tree

"""         DEPTH-FIRST SEARCH         """
def dfs(marker, goals, walls, rows, cols, canvas, cell_size, tree_canvas):
    stack = [(marker, [marker])]
    visited = set()
    parent = {}
    parent[marker] = None  # Root node has no parent
    node_count = 0
    steps = []  # To store each step

    # Create the yellow square
    yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)

    while stack:
        (current, path) = stack.pop()

        if current in visited:
            continue
        visited.add(current)
        node_count += 1

        # Store the current step
        steps.append(('move', current))

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()

        # Move the yellow square to the current node
        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        steps.append(('highlight', current, "lightgray"))  # Save the highlighted step

        time.sleep(0.1)  # Add a delay for better visualization

        if current in goals:
            # Remove the yellow square before playing the final path animation
            canvas.delete(yellow_square)
            directions = convert_path_to_directions(path)
            return path, node_count, directions, parent, steps  # Return the steps

        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
                parent[neighbor] = current  # Track parent

                # Highlight the neighbors being expanded
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                steps.append(('highlight', neighbor, "lightgreen"))  # Save the highlight step
                canvas.update()

                # Render the search tree dynamically
                render_search_tree(parent, tree_canvas)
                steps.append(('tree_update', parent))  # Save the tree update
                time.sleep(0.1)  # Add a delay for neighbor expansion visualization

    return None, node_count, [], parent, steps  # Return the steps

"""         BREADTH-FIRST SEARCH         """
def bfs(marker, goals, walls, rows, cols, canvas, cell_size, tree_canvas):
    """Perform Breadth-First Search (BFS) with visualized search tree changes and node tracking."""
    queue = [(marker, [marker])]  # Queue to manage BFS (FIFO)
    visited = set()  # Keep track of visited nodes
    parent = {}  # Track parent-child relationships
    parent[marker] = None  # Root node has no parent
    node_count = 0  # To track the number of nodes created
    steps = []  # To store each step

    # Create the yellow square
    yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while queue:
        (current, path) = queue.pop(0)  # Dequeue (FIFO)

        if current in visited:
            continue
        visited.add(current)
        node_count += 1  # Count the node

        # Store the current step
        steps.append(('move', current))

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()

        # Move the yellow square to the current node
        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        steps.append(('highlight', current, "lightgray"))  # Save the highlighted step

        time.sleep(0.1)  # Add a delay for better visualization

        # If we reached one of the goals, return the path and parent-child relationships
        if current in goals:
            # Remove the yellow square before playing the final path animation
            canvas.delete(yellow_square)
            directions = convert_path_to_directions(path)
            return path, node_count, directions, parent, steps  # Return the steps

        # Get the possible neighbors (UP, LEFT, DOWN, RIGHT)
        neighbors = get_neighbors_inverted(current, walls, rows, cols)

        # Highlight the neighbors being expanded
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))  # Enqueue neighbors
                parent[neighbor] = current  # Track the parent
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                steps.append(('highlight', neighbor, "lightgreen"))  # Save the highlight step
                canvas.update()

                # Render the search tree dynamically
                render_search_tree(parent, tree_canvas)
                steps.append(('tree_update', parent))  # Save the tree update
                time.sleep(0.1)  # Add a delay for neighbor expansion visualization

    return None, node_count, [], parent, steps  # Return the steps

"""         GREEDY BEST-FIRST SEARCH (GBFS)         """
def gbfs(marker, goals, walls, rows, cols, canvas, cell_size, tree_canvas):
    """Greedy Best-First Search implementation with visualization."""
    open_list = []
    heapq.heappush(open_list, (0, marker))  # priority queue with heuristic values
    came_from = {marker: None}  # Track parent-child relationships
    visited = set()
    visited.add(marker)
    node_count = 0
    directions = []
    steps = []  # To store each step

    # Create the yellow square
    yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while open_list:
        _, current = heapq.heappop(open_list)
        node_count += 1

        # Store the current step
        steps.append(('move', current))

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()

        # Move the yellow square to the current node
        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        steps.append(('highlight', current, "lightgray"))  # Save the highlighted step

        time.sleep(0.1)  # Add a delay for better visualization

        if current in goals:
            # Remove the yellow square before playing the final path animation
            canvas.delete(yellow_square)
            
            # Backtrack to find the path
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()

            # Convert path to directions (up, left, down, right)
            directions = convert_path_to_directions(path)

            # Highlight the final path in blue
            highlight_final_path(canvas, path, cell_size)
            return path, node_count, directions, came_from, steps  # Return the steps

        # Explore neighbors (prioritize based on heuristic)
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                heapq.heappush(open_list, (manhattan_distance(neighbor, goals[0]), neighbor))
                came_from[neighbor] = current  # Track parent-child relationship
                
                # Highlight the neighbors being considered
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                steps.append(('highlight', neighbor, "lightgreen"))  # Save the highlight step
                canvas.update()

                # Render the search tree dynamically
                render_search_tree(came_from, tree_canvas)
                steps.append(('tree_update', came_from))  # Save the tree update
                time.sleep(0.1)  # Add a delay for neighbor visualization

    return None, node_count, [], came_from, steps  # Return the steps

"""         A* SEARCH         """
def a_star(marker, goals, walls, rows, cols, canvas, cell_size, tree_canvas):
    """A* search algorithm implementation with visualized visited nodes."""
    open_list = []  # Priority queue for nodes to be evaluated
    heapq.heappush(open_list, (0, marker))  # Push the starting marker with a priority of 0
    came_from = {marker: None}  # Track parent-child relationships
    g_score = {marker: 0}  # Cost from start to current node
    f_score = {marker: manhattan_distance(marker, goals[0])}  # Estimated total cost from start to goal
    visited = set()
    node_count = 0
    directions = []
    steps = []  # To store each step

    # Create the yellow square
    yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while open_list:
        # Get the node with the lowest f_score
        current = heapq.heappop(open_list)[1]
        node_count += 1

        # Store the current step
        steps.append(('move', current))

        # Highlight the current node as visited (in light gray)
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()

        # Move the yellow square to the current node
        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        steps.append(('highlight', current, "lightgray"))  # Save the highlighted step

        time.sleep(0.1)  # Add a delay for better visualization

        # Check if the current node is a goal
        if current in goals:
            # Remove the yellow square before playing the final path animation
            canvas.delete(yellow_square)
            
            # Backtrack to find the path
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            path.reverse()

            # Convert path to directions (up, left, down, right)
            directions = convert_path_to_directions(path)
            return path, node_count, directions, came_from, steps  # Return the steps

        # Explore neighbors
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1  # Assume cost to neighbor is 1

            # If the neighbor is not visited or found a better path
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current  # Track parent-child relationship
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goals[0])

                # If the neighbor is not already in the open list, add it
                if neighbor not in visited:
                    visited.add(neighbor)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

                # Highlight the neighbor for visualization
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                steps.append(('highlight', neighbor, "lightgreen"))  # Save the highlight step
                canvas.update()

                # Render the search tree dynamically
                render_search_tree(came_from, tree_canvas)
                steps.append(('tree_update', came_from))  # Save the tree update
                time.sleep(0.1)  # Add a delay for neighbor visualization

    return None, node_count, [], came_from, steps  # Return the steps

# Heuristic function (Manhattan distance)
def manhattan_distance(node, goal):
    """Calculate the Manhattan distance from the current node to the goal."""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

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
    """Highlight the final path with red lines."""
    previous_position = None
    for position in path:
        col, row = position
        # Highlight the cell in light blue
        highlight_cell(canvas, position, cell_size, "lightblue")

        # Calculate the midpoint of the current cell
        x_mid = col * cell_size + cell_size / 2
        y_mid = row * cell_size + cell_size / 2

        # If there's a previous position, draw a red line from the previous midpoint to the current midpoint
        if previous_position:
            canvas.create_line(previous_position[0], previous_position[1], x_mid, y_mid, fill="red", width=2)

        # Update the previous position to the current midpoint
        previous_position = (x_mid, y_mid)