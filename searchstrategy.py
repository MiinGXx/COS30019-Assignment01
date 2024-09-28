import time

def dfs_search_visual(start, goals, walls, rows, cols, update_square_callback):
    """Perform Depth-First Search (DFS) with visual updates to show the yellow square's progression."""
    # Define movement directions (UP, LEFT, DOWN, RIGHT)
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # UP, LEFT, DOWN, RIGHT
    direction_names = ["UP", "LEFT", "DOWN", "RIGHT"]

    # Stack for DFS, initialized with the starting position
    stack = [(start, [])]  # (current_position, moves_taken)

    visited = set()  # Set to store visited nodes
    visited.add(start)

    while stack:
        (current_pos, moves) = stack.pop()

        # Visualize the yellow square's current position
        update_square_callback(current_pos)

        # Pause to visualize the step-by-step search process
        time.sleep(0.5)  # Add delay to slow down the animation for visualization

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
