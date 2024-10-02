def dfs(start, goals, walls, rows, cols):
    """
    Perform a Depth-First Search (DFS) to find a path from the start position to any of the goal positions.
    Args:
        start (tuple): The starting position as a tuple (x, y).
        goals (set): A set of goal positions, each as a tuple (x, y).
        walls (set): A set of wall positions, each as a tuple (x, y), representing obstacles.
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
    Returns:
        tuple: A tuple containing the path and the directions taken to reach a goal, or None if no path is found.
            - path (list): A list of positions (tuples) representing the path from start to a goal.
            - path_directions (list): A list of direction names (strings) representing the directions taken.
    """
    stack = [(start, [], [])]  # (current position, path, directions)
    visited = set()
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Up, Left, Down, Right
    direction_names = ["Up", "Left", "Down", "Right"]

    while stack:
        (current, path, path_directions) = stack.pop() # LIFO

        if current in visited: # Skip visited nodes if encountered again
            continue
        visited.add(current) # Mark as visited if not already visited

        path = path + [current] # Add current node to path

        if current in goals: # Check if current node is a goal
            return path, path_directions # Return path and directions

        # Prioritize upward movement and chronological node expansion
        # by reversing the order of directions and direction names
        # to explore the Up, Left, Down, Right order
        for direction, direction_name in reversed(list(zip(directions, direction_names))):
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and
                    neighbor not in walls and neighbor not in visited):
                stack.append((neighbor, path, path_directions + [direction_name]))

    return None