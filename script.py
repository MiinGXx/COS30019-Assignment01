import sys
from tkinter import Tk, Canvas
from grid import create_grid, create_yellow_square, animate_path
from wall import add_wall_coordinates
from searchstrategy import dfs
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

            return rows, cols, (col_idx, row_idx), goals, walls

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Unable to parse grid dimensions or coordinates. {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    rows, cols, marker, goals, walls = parse_input_file(input_file)

    # Perform DFS to find a path to one of the goals
    path, path_directions = dfs(marker, goals, walls, rows, cols)

    if path:
        print("\nPath found to goal:")
        for step, direction in zip(path, path_directions):
            print(f"{step} -> {direction}")

        # Initialize Tkinter window
        root = Tk()
        root.title("DFS Path Animation")
        
        # Create canvas
        canvas = Canvas(root, width=cols * 50, height=rows * 50)
        canvas.pack()

        # Draw the grid
        create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

        # Create the yellow square at the starting position
        yellow_square = create_yellow_square(canvas, marker[0], marker[1])

        # Animate the yellow square along the path
        animate_path(canvas, yellow_square, path)

        # Start Tkinter loop
        root.mainloop()

    else:
        print("\nNo path found to any goal.")

if __name__ == "__main__":
    main()
