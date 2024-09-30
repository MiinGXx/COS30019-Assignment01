import heapq

def dfs_search_store_moves(start, goals, walls, rows, cols, visit_callback=None, explore_callback=None):
    """Perform DFS and visualize the search tree through a callback on each move."""
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # UP, LEFT, DOWN, RIGHT
    direction_names = ["UP", "LEFT", "DOWN", "RIGHT"]

    stack = [(start, [])]  # Stack for DFS, with (current_position, moves_taken)
    visited = set()
    
    move_history = []

    while stack:
        current_pos, moves = stack.pop()
        
        # If already visited, skip this position
        if current_pos in visited:
            continue
            
        visited.add(current_pos)
        
        # Call the callback function to update the grid with visited nodes
        if visit_callback:
            visit_callback(current_pos)

        move_history.append((current_pos, moves))

        print(f"Visiting {current_pos}, Moves: {moves}")  # Debugging statement

        # Check if current position is a goal state
        if current_pos in goals:
            print(f"Goal reached at {current_pos} with moves: {moves}")
            return move_history

        # Explore neighbors
        for i, (d_row, d_col) in enumerate(directions):
            next_pos = (current_pos[0] + d_col, current_pos[1] + d_row)

            # Check boundaries and walls
            if (0 <= next_pos[0] < cols and 0 <= next_pos[1] < rows and
                next_pos not in walls and next_pos not in visited):
                if explore_callback:
                    explore_callback(next_pos)  # Highlight exploring node
                stack.append((next_pos, moves + [direction_names[i]]))

    print("No path to any goal was found.")
    return move_history

def bfs_search_store_moves(start_pos, goals, walls, rows, cols, explore_callback=None, visit_callback=None):
    """BFS to find the path from start_pos to goals while tracking movements."""
    from collections import deque

    direction_names = ["UP", "DOWN", "LEFT", "RIGHT"]  # Define the direction names
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Corresponding (row, col) changes for UP, DOWN, LEFT, RIGHT
    queue = deque([(start_pos, [])])  # Queue for BFS with (position, moves)
    visited = set()  # Track visited nodes

    while queue:
        current_pos, moves = queue.popleft()

        # If already visited, skip this position
        if current_pos in visited:
            continue
        visited.add(current_pos)

        # Execute the visit callback if defined
        if visit_callback:
            visit_callback(current_pos)

        # Check if the current position is a goal
        if current_pos in goals:
            return [(current_pos, moves)]  # Return the final path if goal is reached

        # Explore neighbors
        for i, (dr, dc) in enumerate(directions):
            next_pos = (current_pos[0] + dr, current_pos[1] + dc)

            # Check bounds and wall conditions
            if (0 <= next_pos[0] < cols) and (0 <= next_pos[1] < rows) and (next_pos not in walls):
                # Append to queue with updated moves
                queue.append((next_pos, moves + [direction_names[i]]))

        # Execute the explore callback for all neighbors after processing current_pos
        if explore_callback:
            explore_callback(current_pos)

    print("No path to any goal was found.")
    return []  # Return empty if no path is found
