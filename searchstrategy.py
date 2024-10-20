import time
import heapq
import networkx as nx
import matplotlib.pyplot as plt

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    If the graph is a tree, this will return the positions to plot this in a hierarchical layout.
    Arguments:
        G (networkx.DiGraph): The graph to plot.
        root (tuple): The root node for the tree (should be the starting grid coordinate).
        width (float): Horizontal space allocated for the layout.
        vert_gap (float): Vertical gap between levels of the tree.
        vert_loc (float): The vertical location of the root.
        xcenter (float): The horizontal location of the root.
    Returns:
        pos (dict): A dictionary of positions keyed by node.
    """
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, node, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    """
    Helper function for hierarchy_pos.
    """
    if pos is None:
        pos = {node: (xcenter, vert_loc)}
    else:
        pos[node] = (xcenter, vert_loc)
        
    children = list(G.neighbors(node))
    
    if not isinstance(G, nx.DiGraph):
        raise TypeError("The graph must be a directed graph.")
    
    if not children:
        return pos
    
    dx = width / max(1, len(children))  # Adjust horizontal space based on the number of children
    nextx = xcenter - width / 2 - dx / 2  # Adjust x position to center the children
    
    for child in children:
        nextx += dx
        pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos, parent=node, parsed=parsed)
    
    return pos

def render_search_tree(parent_dict):
    """Render the search tree based on parent-child relationships."""
    G = nx.DiGraph()  # Create a directed graph

    # Add edges based on parent-child relationships
    for child, parent in parent_dict.items():
        if parent is not None:
            G.add_edge(parent, child)

    # Get the root of the tree (starting node) - usually the marker/agent
    root = [node for node in parent_dict if parent_dict[node] is None][0]

    # Use the custom hierarchy layout for the tree
    pos = hierarchy_pos(G, root, width=2.0, vert_gap=0.5)  # Increase width and vertical gap for more space

    # Create a larger plot to accommodate more space
    plt.figure(figsize=(12, 8))  # Adjust the figure size (width, height)

    # Draw the tree with the hierarchical layout
    nx.draw(G, pos, with_labels=True, node_size=300, node_color="lightblue", font_size=8, font_weight="bold", arrows=True)

    plt.title("Search Tree (Top-to-Bottom Layout)")
    plt.show()




"""         DEPTH-FIRST SEARCH         """
def dfs(marker, goals, walls, rows, cols, canvas, cell_size):
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

    return None, node_count, [], parent  # No path found, return parent dictionary anyway




"""         BREADTH-FIRST SEARCH         """
def bfs(marker, goals, walls, rows, cols, canvas, cell_size):
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

    return None, node_count, [], parent  # Return parent-child relationships even if no path found




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

    print("No path to the goal was found.")
    return None, node_count, directions, came_from  # No path found, return parent dict







"""         A* SEARCH         """
def a_star(marker, goals, walls, rows, cols, canvas, cell_size):
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
