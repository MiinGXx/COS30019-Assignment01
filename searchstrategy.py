def dfs(start, goals, walls, rows, cols):
    stack = [(start, [], [])]  # (current position, path, directions)
    visited = set()
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Up, Left, Down, Right
    direction_names = ["Up", "Left", "Down", "Right"]

    while stack:
        (current, path, path_directions) = stack.pop()

        if current in visited:
            continue
        visited.add(current)

        path = path + [current]

        if current in goals:
            return path, path_directions

        # Prioritize upward movement and chronological node expansion
        for direction, direction_name in reversed(list(zip(directions, direction_names))):
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and
                    neighbor not in walls and neighbor not in visited):
                stack.append((neighbor, path, path_directions + [direction_name]))

    return None