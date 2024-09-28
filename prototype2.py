import sys
import re
import tkinter as tk

def add_wall_coordinates(start_col, start_row, width, height):
    """Helper function to calculate all the coordinates occupied by a wall."""
    wall_coords = []
    for row in range(start_row, start_row + height):
        for col in range(start_col, start_col + width):
            wall_coords.append((col, row))
    return wall_coords

def create_grid(canvas, rows, cols, markers=None, goals=None, walls=None):
    """Function to create and display the grid in the Tkinter canvas."""
    cell_size = 50
    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if markers and (col, row) in markers:
                color = "red"
            elif goals and (col, row) in goals:
                color = "green"
            elif walls and (col, row) in walls:
                color = "gray"
            else:
                color = "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

def create_yellow_square(canvas, col, row):
    """Create a smaller yellow square on top of the red marker."""
    cell_size = 50
    square_size = 30  # Smaller size for the yellow square
    x1 = col * cell_size + (cell_size - square_size) / 2
    y1 = row * cell_size + (cell_size - square_size) / 2
    x2 = x1 + square_size
    y2 = y1 + square_size
    return canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black")

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

            # Create GUI window
            window = tk.Tk()
            window.title("Grid Visualization")

            # Create canvas for grid
            canvas = tk.Canvas(window, width=cols * 50, height=rows * 50)
            canvas.pack()

            # Create and display the grid
            create_grid(canvas, rows, cols, markers=[(col_idx, row_idx)], goals=goals, walls=walls)

            # Create the yellow square on top of the marker cell
            yellow_square = create_yellow_square(canvas, col_idx, row_idx)

            window.mainloop()

    except FileNotFoundError: # Catch file not found error
        print(f"Error: The file '{input_file}' was not found.")
    except ValueError as e: # Catch value error
        print(f"Error: Unable to parse grid dimensions or coordinates. {e}")
    except Exception as e: # Catch any other exceptions
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
