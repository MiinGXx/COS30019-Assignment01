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

def gbfs_search_store_moves(start, goals, walls, rows, cols, explore_callback=None, visit_callback=None):
    """Greedy Best-First Search to find the path from start to goals using heuristic."""
    def heuristic(a, b):
        """Heuristic function: Use Manhattan distance between current position and goal."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    direction_names = ["UP", "DOWN", "LEFT", "RIGHT"]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP, DOWN, LEFT, RIGHT

    priority_queue = []  # Priority queue (min-heap) for GBFS
    visited = set()
    heapq.heappush(priority_queue, (0, start, []))  # (heuristic_cost, current_position, moves)

    while priority_queue:
        _, current_pos, moves = heapq.heappop(priority_queue)

        if current_pos in visited:
            continue

        visited.add(current_pos)

        if visit_callback:
            visit_callback(current_pos)
            
        # Check if the current position is a goal
        if current_pos in goals:
            return [(current_pos, moves)]  # Return the final path if goal is reached

        # Explore neighbors
        for i, (dr, dc) in enumerate(directions):
            next_pos = (current_pos[0] + dr, current_pos[1] + dc)

            # Check bounds and walls
            if (0 <= next_pos[0] < cols and 0 <= next_pos[1] < rows and next_pos not in walls):
                heuristic_cost = min(heuristic(next_pos, goal) for goal in goals)
                heapq.heappush(priority_queue, (heuristic_cost, next_pos, moves + [direction_names[i]]))

                if explore_callback:
                    explore_callback(next_pos)

    print("No path to any goal was found.")
    return []

def heuristic(a, b):

    """Calculate the Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, walls, rows, cols):
    """Return valid neighbors for the given position."""
    x, y = pos
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        neighbor = (x + dx, y + dy)
        if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows and neighbor not in walls:
            neighbors.append(neighbor)
    return neighbors

def reconstruct_path(came_from, current):
    """Reconstruct the path from start to goal."""
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]  # Return reversed path

def astar_search_store_moves(start, goals, walls, rows, cols, explore_callback=None, visit_callback=None):
    """Perform A* search and store moves."""
    open_set = []
    heapq.heappush(open_set, (0, start))  # Priority queue
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: heuristic(start, goals[0])}  # Assuming a single goal for simplicity

    move_history = []  # To store the positions explored
    
    while open_set:
        current = heapq.heappop(open_set)[1]

        if current in goals:
            path = reconstruct_path(came_from, current)
            return [(pos, 'goal') for pos in path]  # Return goal path with 'goal' marker
        
        if explore_callback:
            explore_callback(current)
            move_history.append((current, 'exploring'))  # Store explored nodes

        for neighbor in get_neighbors(current, walls, rows, cols):
            tentative_g_score = g_score[current] + 1  # Cost from start to neighbor

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goals[0])
                
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

            if visit_callback:
                visit_callback(neighbor)

    return move_history  # Return move history if no path found