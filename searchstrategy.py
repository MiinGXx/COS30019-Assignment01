import time
import heapq
import tkinter as tk

def new_render_search_tree_tk(parent_dict, canvas, node_radius=20, x_gap=100, y_gap=100):
    """
    Render the search tree dynamically on the canvas.
    Each node will be drawn in a tree structure with parent-child connections.
    """
    canvas.delete("all")  # Clear any previous drawing

    # Calculate the canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Dictionary to store the positions of each node (key=node, value=(x, y))
    node_positions = {}

    # Function to calculate the width of the subtree rooted at a given node
    def calculate_subtree_width(node):
        children = [child for child, parent in parent_dict.items() if parent == node]
        if not children:
            return 1  # Leaf nodes take up a width of 1 unit

        # Sum up the widths of all child subtrees
        subtree_width = 0
        for child in children:
            child_subtree_width = calculate_subtree_width(child)
            subtree_width += child_subtree_width

        return max(subtree_width, len(children))  # Ensure width is large enough for splitting

    # Recursive function to assign positions based on dynamically updated subtree width
    def assign_positions(node, depth, x_offset):
        # Calculate the width of the subtree rooted at this node
        subtree_width = calculate_subtree_width(node)

        # The x position is the middle of this subtree
        x = x_offset + (subtree_width / 2) * x_gap
        y = depth * y_gap
        node_positions[node] = (x, y)

        # Now, assign positions to the children
        children = [child for child, parent in parent_dict.items() if parent == node]
        if children:
            total_width = sum(calculate_subtree_width(child) for child in children)
            current_x_offset = x_offset

            # Adjust child positions evenly around the parent node
            for child in children:
                child_width = calculate_subtree_width(child)
                assign_positions(child, depth + 1, current_x_offset)
                current_x_offset += child_width * x_gap

    # Find the root (node with no parent)
    root = [node for node in parent_dict if parent_dict[node] is None][0]

    # Calculate the total width of the tree
    total_tree_width = calculate_subtree_width(root)

    # Assign positions to all nodes, starting from the root
    assign_positions(root, 0, 0)

    # Calculate the horizontal offset to center the tree on the canvas
    total_tree_pixel_width = total_tree_width * x_gap
    center_offset = (canvas_width - total_tree_pixel_width) // 2

    # Draw the edges (arrows) first, so they appear behind the nodes
    for node, (x, y) in node_positions.items():
        x += center_offset  # Apply centering offset to each node's x position
        if parent_dict[node] is not None:
            parent_x, parent_y = node_positions[parent_dict[node]]
            parent_x += center_offset
            canvas.create_line(parent_x, parent_y + node_radius, x, y - node_radius, fill="black", width=2)

    # Draw the nodes on top of the arrows
    for node, (x, y) in node_positions.items():
        x += center_offset  # Apply centering offset
        # Draw the node as a circle
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(node), font=("Arial", 10, "bold"))

    # Update the canvas display
    canvas.update()










"""         DEPTH-FIRST SEARCH         """
def dfs(marker, goals, walls, rows, cols, canvas, cell_size, tree_canvas):
    stack = [(marker, [marker])]
    visited = set()
    parent = {}
    parent[marker] = None  # Root node has no parent
    node_count = 0

    # Visualize the initial marker
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while stack:
        (current, path) = stack.pop()

        if current in visited:
            continue
        visited.add(current)
        node_count += 1

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()
        time.sleep(0.1)  # Add a delay for better visualization

        if current in goals:
            directions = convert_path_to_directions(path)
            return path, node_count, directions, parent  # Return parent dict

        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
                parent[neighbor] = current  # Track parent

                # Highlight the neighbors being expanded
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.1)  # Add a delay for neighbor expansion visualization

                # Render the search tree dynamically
                new_render_search_tree_tk(parent, tree_canvas)

    return None, node_count, [], parent  # No path found, return parent dictionary anyway





"""         BREADTH-FIRST SEARCH         """
def bfs(marker, goals, walls, rows, cols, canvas, cell_size, tree_canvas):
    """Perform Breadth-First Search (BFS) with visualized search tree changes and node tracking."""
    queue = [(marker, [marker])]  # Queue to manage BFS (FIFO)
    visited = set()  # Keep track of visited nodes
    parent = {}  # Track parent-child relationships
    parent[marker] = None  # Root node has no parent
    node_count = 0  # To track the number of nodes created

    # Visualize the initial marker
    highlight_cell(canvas, marker, cell_size, "yellow")
    canvas.update()

    while queue:
        (current, path) = queue.pop(0)  # Dequeue (FIFO)

        if current in visited:
            continue
        visited.add(current)
        node_count += 1  # Count the node

        # Highlight the current node as visited
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()
        time.sleep(0.1)  # Add a delay for better visualization

        # If we reached one of the goals, return the path and parent-child relationships
        if current in goals:
            directions = convert_path_to_directions(path)
            return path, node_count, directions, parent  # Return parent dict

        # Get the possible neighbors (UP, LEFT, DOWN, RIGHT)
        neighbors = get_neighbors_inverted(current, walls, rows, cols)

        # Highlight the neighbors being expanded
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))  # Enqueue neighbors
                parent[neighbor] = current  # Track the parent
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.1)  # Add a delay for neighbor expansion visualization

                # Render the search tree dynamically
                new_render_search_tree_tk(parent, tree_canvas)

    return None, node_count, [], parent  # Return parent-child relationships even if no path found




"""         GREEDY BEST-FIRST SEARCH (GBFS)         """
# Heuristic function (Manhattan distance)
def manhattan_distance(node, goal):
    """Calculate the Manhattan distance from the current node to the goal."""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# Greedy Best-First Search (GBFS)
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
            directions = convert_path_to_directions(path)

            # Highlight the final path in blue
            highlight_final_path(canvas, path, cell_size)
            return path, node_count, directions, came_from  # Return parent-child relationships

        # Explore neighbors (prioritize based on heuristic)
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                heapq.heappush(open_list, (manhattan_distance(neighbor, goals[0]), neighbor))
                came_from[neighbor] = current  # Track parent-child relationship
                
                # Highlight the neighbors being considered
                highlight_cell(canvas, neighbor, cell_size, "lightgreen")
                canvas.update()
                time.sleep(0.1)  # Delay for neighbor visualization

                # Render the search tree dynamically
                new_render_search_tree_tk(came_from, tree_canvas)

    print("No path to the goal was found.")
    return None, node_count, directions, came_from  # No path found, return parent dict







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

    while open_list:
        # Get the node with the lowest f_score
        current = heapq.heappop(open_list)[1]
        node_count += 1

        # Highlight the current node as visited (in light gray)
        highlight_cell(canvas, current, cell_size, "lightgray")
        canvas.update()  # Update the canvas for animation
        time.sleep(0.1)  # Add a delay for better visualization

        # Check if the current node is a goal
        if current in goals:
            # Backtrack to find the path
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            path.reverse()

            # Convert path to directions (up, left, down, right)
            directions = convert_path_to_directions(path)
            return path, node_count, directions, came_from  # Return parent dict

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
                canvas.update()
                time.sleep(0.1)  # Add a delay for neighbor visualization

                # Render the search tree dynamically
                new_render_search_tree_tk(came_from, tree_canvas)

    print("No path to the goal was found.")
    return None, node_count, directions, came_from  # No path found




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
