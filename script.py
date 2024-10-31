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
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <method> [weight] [multiple]")
        sys.exit(1)

    input_file = sys.argv[1]
    method = sys.argv[2].upper()

    # Handle optional arguments based on the method chosen
    weight = None
    find_multiple_paths = False

    if method == "WAS":
        if len(sys.argv) < 4:
            print("Error: Weighted A* requires a weight as the third argument.")
            sys.exit(1)
        try:
            weight = float(sys.argv[3])
        except ValueError:
            print("Error: Weight must be a numeric value.")
            sys.exit(1)

        # Check for the optional 'multiple' argument for finding multiple goals
        if len(sys.argv) == 5 and sys.argv[4].lower() == "multiple":
            find_multiple_paths = True

    elif len(sys.argv) == 4 and sys.argv[3].lower() == "multiple":
        find_multiple_paths = True

    # Parse the input file
    rows, cols, marker, goals, walls = parse_input_file(input_file)

    # Create and display the grid in the GUI with the option for multiple paths
    create_grid_window(rows, cols, marker, goals, walls, method, weight, find_multiple_paths)

if __name__ == "__main__":
    main()
