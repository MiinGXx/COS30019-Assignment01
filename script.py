import sys
from gui import create_grid_window
from wall import add_wall_coordinates
import re

def parse_input_file(input_file):
    """Parse the input file to extract grid dimensions, marker, goals, and walls."""
    try:
        with open(input_file, 'r') as file:
            # First line: grid dimensions
            first_line = file.readline().strip()
            grid_line = first_line.split(']')[0] + ']'
            grid_dimensions = grid_line.strip('[]').split(',')
            rows, cols = int(grid_dimensions[0].strip()), int(grid_dimensions[1].strip())

            # Second line: marker coordinates
            second_line = file.readline().strip()
            coord_line = second_line.split(')')[0] + ')'
            coordinates = coord_line.strip('()').split(',')
            col_idx, row_idx = int(coordinates[0].strip()), int(coordinates[1].strip())

            # Third line: goal states
            third_line = file.readline().strip()
            goal_coords = re.findall(r'\((\d+),\s*(\d+)\)', third_line)
            goals = [(int(col), int(row)) for col, row in goal_coords]

            # Remaining lines: walls
            walls = []
            for line in file:
                line = line.strip()
                if line.startswith('('):
                    wall_data = re.findall(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', line)
                    for (start_col, start_row, width, height) in wall_data:
                        wall_coords = add_wall_coordinates(int(start_col), int(start_row), int(width), int(height))
                        walls.extend(wall_coords)

        return rows, cols, (col_idx, row_idx), goals, walls

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Unable to parse grid dimensions or coordinates. {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <strategy>")
        print("Strategies: 'DFS' for Depth-First Search, 'BFS' for Breadth-First Search,'GBFS' for Greedy Best-First Search, or 'AS' for A* Search.")
        sys.exit(1)

    input_file = sys.argv[1]
    strategy = sys.argv[2].strip().upper()  # Convert strategy to uppercase for consistency

    # Validate the strategy
    if strategy not in ['DFS', 'BFS', 'GBFS', 'AS']:
        print("Error: Invalid strategy. Please use 'DFS', 'BFS', 'GBFS', or 'AS'.")
        sys.exit(1)

    rows, cols, marker, goals, walls = parse_input_file(input_file)

    # Create and display the grid in the GUI
    create_grid_window(rows, cols, marker, goals, walls, strategy)

if __name__ == "__main__":
    main()
