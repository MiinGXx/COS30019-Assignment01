import sys
import re

def display_grid(rows, cols, markers=None, goals=None, walls=None):
    """Function to display the grid based on given rows and columns.
    - Markers is a list of (col, row) coordinates to place an 'X'.
    - Goals is a list of (col, row) coordinates to place an 'O'.
    - Walls is a list of coordinates occupied by walls to place '#'.
    """
    for row in range(rows):
        row_display = []
        for col in range(cols):
            if markers and (col, row) in markers:
                row_display.append('X')  # Mark the specified coordinate with 'X'
            elif goals and (col, row) in goals:
                row_display.append('O')  # Mark the goal coordinates with 'O'
            elif walls and (col, row) in walls:
                row_display.append('#')  # Mark the wall coordinates with '#'
            else:
                row_display.append('.')
        print(' '.join(row_display))

def add_wall_coordinates(start_col, start_row, width, height):
    """Helper function to calculate all the coordinates occupied by a wall."""
    wall_coords = []
    for row in range(start_row, start_row + height):
        for col in range(start_col, start_col + width):
            wall_coords.append((col, row))
    return wall_coords

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

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            # First line: grid dimensions
            first_line = file.readline().strip()
            grid_line = first_line.split(']')[0] + ']'
            grid_dimensions = grid_line.strip('[]').split(',')
            rows, cols = int(grid_dimensions[0].strip()), int(grid_dimensions[1].strip())

            # Second line: marker coordinates (column index, row index)
            second_line = file.readline().strip()
            coord_line = second_line.split(')')[0] + ')'
            coordinates = coord_line.strip('()').split(',')
            col_idx, row_idx = int(coordinates[0].strip()), int(coordinates[1].strip())

            # Third line: goal states (coordinates) e.g. (7,0) | (10,3)
            third_line = file.readline().strip()
            goal_coords = re.findall(r'\((\d+),\s*(\d+)\)', third_line)
            goals = [(int(col), int(row)) for col, row in goal_coords]

            # Read the remaining lines for walls
            walls = []
            for line in file:
                line = line.strip()
                if line.startswith('('):
                    # Parse the wall coordinates and dimensions (col, row, width, height)
                    wall_data = re.findall(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', line)
                    for (start_col, start_row, width, height) in wall_data:
                        wall_coords = add_wall_coordinates(int(start_col), int(start_row), int(width), int(height))
                        walls.extend(wall_coords)

            print(f"Grid Dimensions: {rows} rows, {cols} columns")
            print(f"Marker at: (Column: {col_idx}, Row: {row_idx})")
            print(f"Goal states at: {goals}")
            print(f"Walls at: {walls}")
            
            print("\nGenerated Grid:")
            display_grid(rows, cols, markers=[(col_idx, row_idx)], goals=goals, walls=walls)

            # Perform DFS to find a path to one of the goals
            start = (col_idx, row_idx)
            path, path_directions = dfs(start, goals, walls, rows, cols)
            if path:
                print("\nPath to goal:")
                for step, direction in zip(path, path_directions):
                    print(f"{step} -> {direction}")
            else:
                print("\nNo path found to any goal.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except ValueError as e:
        print(f"Error: Unable to parse grid dimensions or coordinates. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
