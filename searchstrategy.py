def dfs_search(start, goals, walls, rows, cols):
    """Perform Depth-First Search (DFS) to navigate the yellow square to one of the green cells."""
    # Define movement directions (UP, LEFT, DOWN, RIGHT)
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # UP, LEFT, DOWN, RIGHT
    direction_names = ["UP", "LEFT", "DOWN", "RIGHT"]

    # Stack for DFS, initialized with the starting position
    stack = [(start, [])]  # (current_position, moves_taken)

    visited = set()  # Set to store visited nodes
    visited.add(start)

    while stack:
        (current_pos, moves) = stack.pop()

        # Check if current position is a goal state
        if current_pos in goals:
            print(f"Goal reached at {current_pos} with moves: {moves}")
            return moves

        # Explore neighbors in the order: UP, LEFT, DOWN, RIGHT
        for i, (d_row, d_col) in enumerate(directions):
            next_pos = (current_pos[0] + d_col, current_pos[1] + d_row)

            # Check boundaries and walls
            if 0 <= next_pos[0] < cols and 0 <= next_pos[1] < rows and next_pos not in walls and next_pos not in visited:
                visited.add(next_pos)
                # Add to stack (DFS adds to stack, LIFO order)
                stack.append((next_pos, moves + [direction_names[i]]))

    print("No path to any goal was found.")
    return None
