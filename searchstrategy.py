def dfs_search_store_moves(start, goals, walls, rows, cols, visit_callback=None, explore_callback=None):
    """Perform DFS and visualize the search tree through a callback on each move."""
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # UP, LEFT, DOWN, RIGHT
    direction_names = ["UP", "LEFT", "DOWN", "RIGHT"]

    stack = [(start, [])]  # Stack for DFS, with (current_position, moves_taken)
    visited = set()
    visited.add(start)

    move_history = []

    while stack:
        current_pos, moves = stack.pop()

        # Call the callback function to update the grid with visited nodes
        if visit_callback:
            visit_callback(current_pos)

        move_history.append((current_pos, moves))

        # Print the current position and moves for debugging
        print(f"Visiting {current_pos}, Moves: {moves}")

        # Check if current position is a goal state
        if current_pos in goals:
            print(f"Goal reached at {current_pos} with moves: {moves}")
            return move_history

        # Explore neighbors
        for i, (d_row, d_col) in enumerate(directions):
            next_pos = (current_pos[0] + d_col, current_pos[1] + d_row)

            # Check boundaries and walls
            if 0 <= next_pos[0] < cols and 0 <= next_pos[1] < rows and next_pos not in walls and next_pos not in visited:
                visited.add(next_pos)
                if explore_callback:
                    explore_callback(next_pos)  # Highlight exploring node
                stack.append((next_pos, moves + [direction_names[i]]))

    print("No path to any goal was found.")
    return move_history
