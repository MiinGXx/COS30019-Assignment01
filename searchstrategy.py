import time
import heapq
from collections import deque
from grid import create_yellow_square, move_yellow_square, highlight_final_path


def dfs(marker, goals, walls, rows, cols, canvas, cell_size, find_multiple_paths=False):
    full_path = []
    node_count = 0
    steps = []
    remaining_goals = set(goals)
    highlighted_nodes = []
    global_visited = set()  # Global set to keep track of all visited nodes

    while remaining_goals:
        stack = [(marker, [marker])]
        visited = set()
        parent = {marker: None}
        yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)

        while stack:
            current, path = stack.pop()

            if current in visited:
                continue
            visited.add(current)
            global_visited.add(current)
            node_count += 1
            steps.append(('move', current))

            # Move yellow square and highlight visited node in light gray
            rect_id = canvas.create_rectangle(
                current[0] * cell_size, current[1] * cell_size,
                (current[0] + 1) * cell_size, (current[1] + 1) * cell_size,
                fill="lightgray", outline="black"
            )
            highlighted_nodes.append(rect_id)
            move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
            canvas.update()
            time.sleep(0.01)

            # Goal check
            if current in remaining_goals:
                remaining_goals.remove(current)
                canvas.delete(yellow_square)

                # Accumulate the path to this goal
                if full_path and full_path[-1] == path[0]:
                    full_path.extend(path[1:])
                else:
                    full_path.extend(path)

                # If not finding multiple paths, exit after reaching the first goal
                if not find_multiple_paths:
                    directions = convert_path_to_directions(full_path)
                    return full_path, node_count, directions, parent, steps

                # Clear the highlighted nodes
                for node_id in highlighted_nodes:
                    canvas.delete(node_id)
                highlighted_nodes.clear()

                # Reset for the next goal
                marker = current  # Start next search from the current goal
                break  # Exit the inner while loop to start the next search

            # Expand neighbors
            neighbors = get_neighbors(current, walls, rows, cols)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
                    parent[neighbor] = current
                    # Highlight expanded node in light green
                    rect_id = canvas.create_rectangle(
                        neighbor[0] * cell_size, neighbor[1] * cell_size,
                        (neighbor[0] + 1) * cell_size, (neighbor[1] + 1) * cell_size,
                        fill="lightgreen", outline="black"
                    )
                    highlighted_nodes.append(rect_id)
                    canvas.update()
                    time.sleep(0.01)
        else:
            # If stack is empty and goals remain, but no path is found
            if remaining_goals:
                print("No path found to remaining goals.")
                directions = convert_path_to_directions(full_path)
                return full_path, node_count, directions, parent, steps

    canvas.delete(yellow_square)
    directions = convert_path_to_directions(full_path)
    return full_path, node_count, directions, parent, steps





def bfs(marker, goals, walls, rows, cols, canvas, cell_size, find_multiple_paths=False):
    queue = deque([(marker, [marker])])
    visited = set()
    parent = {marker: None}
    node_count = 0
    steps = []
    full_path = []
    remaining_goals = set(goals)
    yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)
    highlighted_nodes = []

    while queue and remaining_goals:
        current, path = queue.popleft()

        if current in visited:
            continue
        visited.add(current)
        node_count += 1
        steps.append(('move', current))

        # Move yellow square and highlight the current node as visited (lightgray)
        rect_id = canvas.create_rectangle(current[0] * cell_size, current[1] * cell_size,
                                          (current[0] + 1) * cell_size, (current[1] + 1) * cell_size,
                                          fill="lightgray", outline="black")
        highlighted_nodes.append(rect_id)
        canvas.update()
        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        time.sleep(0.01)

        # Goal check
        if current in remaining_goals:
            remaining_goals.remove(current)
            # remove the yellow square if the goal is reached
            canvas.delete(yellow_square)
            # Reconstruct and accumulate the path to this goal
            goal_path = reconstruct_path(parent, current)
            full_path.extend(goal_path)

            # If not finding multiple paths, exit after reaching the first goal
            if not find_multiple_paths:
                directions = convert_path_to_directions(full_path)
                return full_path, node_count, directions, parent, steps

            # Clear the highlighted nodes
            for node_id in highlighted_nodes:
                canvas.delete(node_id)
            highlighted_nodes.clear()

            # Reset the queue and visited set for the next goal
            queue = deque([(current, [current])])
            visited = set()
            parent = {current: None}
            # Redraw the yellow square at the current position
            yellow_square = create_yellow_square(canvas, current[0], current[1], cell_size)

        # Expand neighbors
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                parent[neighbor] = current
                # Highlight expanded node in light green
                rect_id = canvas.create_rectangle(neighbor[0] * cell_size, neighbor[1] * cell_size,
                                                  (neighbor[0] + 1) * cell_size, (neighbor[1] + 1) * cell_size,
                                                  fill="lightgreen", outline="black")
                highlighted_nodes.append(rect_id)
                canvas.update()
                time.sleep(0.01)

    canvas.delete(yellow_square)
    directions = convert_path_to_directions(full_path)
    return full_path, node_count, directions, parent, steps

def gbfs(marker, goals, walls, rows, cols, canvas, cell_size, find_multiple_paths=False):
    open_list = []
    heapq.heappush(open_list, (0, marker))
    closed_list = set()
    came_from = {marker: None}
    node_count = 0
    steps = []
    full_path = []
    remaining_goals = set(goals)
    yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)
    highlighted_nodes = []

    while open_list:
        # Extract the node with the lowest heuristic
        _, current = heapq.heappop(open_list)

        if current in closed_list:
            continue

        closed_list.add(current)
        node_count += 1
        steps.append(('move', current))

        # Move the yellow square to the current node and highlight it as visited (light gray)
        if current not in goals:
            rect_id = canvas.create_rectangle(current[0] * cell_size, current[1] * cell_size,
                                              (current[0] + 1) * cell_size, (current[1] + 1) * cell_size,
                                              fill="lightgray", outline="black")
            highlighted_nodes.append(rect_id)

        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        canvas.update()
        time.sleep(0.01)

        # Goal check
        if current in remaining_goals:
            remaining_goals.remove(current)
            canvas.delete(yellow_square)
            # Reconstruct and accumulate the path to this goal
            goal_path = reconstruct_path(came_from, current)
            full_path.extend(goal_path)

            # If not finding multiple paths, exit after reaching the first goal
            if not find_multiple_paths:
                directions = convert_path_to_directions(full_path)
                return full_path, node_count, directions, came_from, steps

            # Clear the highlighted nodes
            for node_id in highlighted_nodes:
                canvas.delete(node_id)
            highlighted_nodes.clear()

            # Reset open list and visited set for the next goal, keeping the previously found path
            open_list = []
            heapq.heappush(open_list, (0, current))
            came_from = {current: None}
            yellow_square = create_yellow_square(canvas, current[0], current[1], cell_size)

        # Expand neighbors with updated heuristic for remaining goals
        neighbors = get_neighbors(current, walls, rows, cols)
        if remaining_goals:  # Ensure remaining_goals is not empty
            for neighbor in neighbors:
                if neighbor not in closed_list and neighbor not in [item[1] for item in open_list]:
                    # Calculate heuristic only based on the nearest remaining goal
                    heuristic = min(manhattan_distance(neighbor, goal) for goal in remaining_goals)
                    heapq.heappush(open_list, (heuristic, neighbor))
                    came_from[neighbor] = current
                    # Highlight expanded node in light green
                    rect_id = canvas.create_rectangle(neighbor[0] * cell_size, neighbor[1] * cell_size,
                                                      (neighbor[0] + 1) * cell_size, (neighbor[1] + 1) * cell_size,
                                                      fill="lightgreen", outline="black")
                    highlighted_nodes.append(rect_id)
                    canvas.update()
                    time.sleep(0.01)

    canvas.delete(yellow_square)    
    directions = convert_path_to_directions(full_path)
    return full_path, node_count, directions, came_from, steps



def a_star(marker, goals, walls, rows, cols, canvas, cell_size, find_multiple_paths=False):
    open_list = []
    heapq.heappush(open_list, (0, 0, marker))  # (f_score, g_score, position)

    came_from = {marker: None}
    g_score = {marker: 0}
    f_score = {marker: min(manhattan_distance(marker, goal) for goal in goals)}
    visited = set()
    node_count = 0
    steps = []
    full_path = []
    remaining_goals = set(goals)
    yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)
    highlighted_nodes = []

    while open_list and remaining_goals:
        # Extract the node with the lowest f_score
        current_f, current_g, current = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)
        node_count += 1
        steps.append(('move', current))

        # Move yellow square and highlight visited node in light gray
        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        rect_id = canvas.create_rectangle(current[0] * cell_size, current[1] * cell_size,
                                          (current[0] + 1) * cell_size, (current[1] + 1) * cell_size,
                                          fill="lightgray", outline="black")
        highlighted_nodes.append(rect_id)
        canvas.update()
        time.sleep(0.01)

        # Goal check
        if current in remaining_goals:
            remaining_goals.remove(current)
            goal_path = reconstruct_path(came_from, current)
            full_path.extend(goal_path)
            canvas.delete(yellow_square)

            # Clear the highlighted nodes
            for node_id in highlighted_nodes:
                canvas.delete(node_id)
            highlighted_nodes.clear()

            # If not finding multiple paths or no remaining goals, end search
            if not find_multiple_paths or not remaining_goals:
                if not remaining_goals:
                    highlight_final_path(canvas, full_path, goals)  # Highlight the final path after all goals are found
                directions = convert_path_to_directions(full_path)
                return full_path, node_count, directions, visited, steps

            # Reset search for next goal: clear open list, visited set, and adjust cost tracking
            open_list = [(0, 0, current)]
            visited = set()
            came_from = {current: None}
            g_score = {current: 0}
            f_score = {current: min(manhattan_distance(current, goal) for goal in remaining_goals)}
            yellow_square = create_yellow_square(canvas, current[0], current[1], cell_size)

        # Expand neighbors
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + min(manhattan_distance(neighbor, goal) for goal in remaining_goals)
                heapq.heappush(open_list, (f_score[neighbor], tentative_g_score, neighbor))
                # Highlight expanded node in light green
                rect_id = canvas.create_rectangle(neighbor[0] * cell_size, neighbor[1] * cell_size,
                                                  (neighbor[0] + 1) * cell_size, (neighbor[1] + 1) * cell_size,
                                                  fill="lightgreen", outline="black")
                highlighted_nodes.append(rect_id)
                canvas.update()
                time.sleep(0.01)

    directions = convert_path_to_directions(full_path)
    return full_path, node_count, directions, visited, steps

def iddfs(marker, goals, walls, rows, cols, canvas, cell_size, find_multiple_paths=False):
    remaining_goals = set(goals)
    steps = []
    full_path = []
    node_count = 0
    directions = []
    iterations = 0  # Track the number of iterations

    # Run IDDFS for each goal independently if find_multiple_paths is True
    while remaining_goals:
        for depth in range(0, 100):  # Arbitrary depth limit, can be adjusted
            iterations += 1  # Increment iteration count
            # Perform Depth-Limited Search (DLS) for the current starting point
            path, new_directions, new_steps, found_goals, highlighted_nodes = dls(
                marker, remaining_goals, walls, rows, cols, depth, canvas, cell_size, find_multiple_paths
            )
            steps.extend(new_steps)  # Record steps for visualization

            # Clear highlighted nodes after each depth iteration
            for node_id in highlighted_nodes:
                canvas.delete(node_id)
            
            if path:
                # Append path and directions to the final results
                if full_path and full_path[-1] == path[0]:
                    full_path.extend(path[1:])  # Avoid duplicating starting point
                else:
                    full_path.extend(path)
                directions.extend(new_directions)
                node_count += len(new_steps)

                # Remove the found goal from remaining_goals
                remaining_goals.difference_update(found_goals)
                marker = path[-1]  # Update marker to new starting point (last goal found)
                
                break  # Restart IDDFS for the next goal if found

        # Exit if no remaining goals or only looking for a single path
        if not find_multiple_paths or not remaining_goals:
            break

    return full_path, node_count, directions, {}, steps, iterations  # Return the accumulated path, count, directions, etc.

def dls(node, goals, walls, rows, cols, depth_limit, canvas, cell_size, find_multiple_paths):
    stack = [(node, [node], 0)]
    visited = set()
    steps = []
    remaining_goals = set(goals)
    highlighted_nodes = []
    yellow_square = create_yellow_square(canvas, node[0], node[1], cell_size)

    while stack:
        current, path, depth = stack.pop()

        # Skip if node is visited or depth exceeds the limit
        if current in visited or depth > depth_limit:
            continue
        visited.add(current)
        steps.append(('move', current))

        # Highlight the current node as visited and move the yellow square
        rect_id = canvas.create_rectangle(
            current[0] * cell_size, current[1] * cell_size,
            (current[0] + 1) * cell_size, (current[1] + 1) * cell_size,
            fill="lightgray", outline="black"
        )
        highlighted_nodes.append(rect_id)
        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        canvas.update()
        time.sleep(0.001)

        # Check if current node is a goal
        if current in remaining_goals:
            remaining_goals.remove(current)
            directions = convert_path_to_directions(path)
            canvas.delete(yellow_square)
            return path, directions, steps, {current}, highlighted_nodes  # Return when a goal is reached

        # Expand neighbors up to depth limit
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor], depth + 1))
                # Highlight expanded node in light green
                rect_id = canvas.create_rectangle(
                    neighbor[0] * cell_size, neighbor[1] * cell_size,
                    (neighbor[0] + 1) * cell_size, (neighbor[1] + 1) * cell_size,
                    fill="lightgreen", outline="black"
                )
                highlighted_nodes.append(rect_id)
                canvas.update()
                time.sleep(0.001)

    # Clean up and return if no goal was found within depth limit
    canvas.delete(yellow_square)
    return None, None, steps, remaining_goals, highlighted_nodes  # Goal not found within depth limit



def weighted_astar(marker, goals, walls, rows, cols, canvas, cell_size, weight, find_multiple_paths=False):
    open_list = []
    heapq.heappush(open_list, (0, marker))  # Initialize with starting node
    came_from = {marker: None}
    g_score = {marker: 0}
    f_score = {marker: weight * min(manhattan_distance(marker, goal) for goal in goals)}
    node_count = 0
    visited = set()
    steps = []
    full_path = []
    remaining_goals = set(goals)
    yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)
    highlighted_nodes = []

    while open_list and remaining_goals:
        _, current = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)
        node_count += 1
        steps.append(('move', current))

        # Move yellow square and highlight visited node in light gray
        rect_id = canvas.create_rectangle(current[0] * cell_size, current[1] * cell_size,
                                          (current[0] + 1) * cell_size, (current[1] + 1) * cell_size,
                                          fill="lightgray", outline="black")
        highlighted_nodes.append(rect_id)
        move_yellow_square(canvas, yellow_square, current[0], current[1], cell_size)
        canvas.update()
        time.sleep(0.01)

        # Goal check
        if current in remaining_goals:
            remaining_goals.remove(current)
            goal_path = reconstruct_path(came_from, current)
            full_path.extend(goal_path)
            canvas.delete(yellow_square)

            # Highlight the completed path segment to the current goal in blue
            highlight_final_path(canvas, full_path, goals)

            # Clear all highlights if there are remaining goals
            if remaining_goals:
                for node_id in highlighted_nodes:
                    canvas.delete(node_id)
                highlighted_nodes.clear()
                open_list = [(0, current)]
                visited = set()
                came_from = {current: None}
                g_score = {current: 0}
                f_score = {current: weight * min(manhattan_distance(current, goal) for goal in remaining_goals)}
                yellow_square = create_yellow_square(canvas, current[0], current[1], cell_size)

            # If all goals are reached or find_multiple_paths=False, end the search
            if not find_multiple_paths or not remaining_goals:
                if not remaining_goals:
                    highlight_final_path(canvas, full_path, goals)  # Highlight the final path
                directions = convert_path_to_directions(full_path)
                return full_path, node_count, directions, came_from, steps

        # Expand neighbors based on weighted cost
        neighbors = get_neighbors(current, walls, rows, cols)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + weight * min(manhattan_distance(neighbor, goal) for goal in remaining_goals)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
                # Highlight expanded node in light green
                rect_id = canvas.create_rectangle(neighbor[0] * cell_size, neighbor[1] * cell_size,
                                                  (neighbor[0] + 1) * cell_size, (neighbor[1] + 1) * cell_size,
                                                  fill="lightgreen", outline="black")
                highlighted_nodes.append(rect_id)
                canvas.update()
                time.sleep(0.01)

    # If all goals are found, return the full path and other details
    directions = convert_path_to_directions(full_path)
    return full_path, node_count, directions, visited, steps

# Helper Functions
def reconstruct_path(came_from, current):
    """Reconstruct the path from start to the current position."""
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def convert_path_to_directions(path):
    """Convert a path to human-readable directions (up, down, left, right)."""
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

def manhattan_distance(node, goal):
    """Calculate Manhattan distance from node to goal."""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def get_neighbors(cell, walls, rows, cols):
    """Get valid neighbors of a cell (UP, LEFT, DOWN, RIGHT) that are not walls."""
    col, row = cell
    neighbors = []
    if col < cols - 1 and (col + 1, row) not in walls:
        neighbors.append((col + 1, row))  # RIGHT
    if row < rows - 1 and (col, row + 1) not in walls:
        neighbors.append((col, row + 1))  # DOWN
    if col > 0 and (col - 1, row) not in walls:
        neighbors.append((col - 1, row))  # LEFT
    if row > 0 and (col, row - 1) not in walls:
        neighbors.append((col, row - 1))  # UP
    return neighbors
