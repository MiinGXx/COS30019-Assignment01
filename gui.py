import tkinter as tk
from grid import create_grid, create_yellow_square, animate_path
from searchstrategy import dfs, bfs, gbfs, a_star, highlight_final_path

def create_grid_window(rows, cols, marker, goals, walls, method, cell_size=50):
    """Create and display the Tkinter GUI window with the grid and animate the yellow square to the goal."""
    window = tk.Tk()
    window.title("Grid Visualization")

    # Create canvas for grid
    canvas = tk.Canvas(window, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    # Create and display the grid
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

    # Perform the search based on the chosen method
    if method == "DFS":
        path, node_count, directions = dfs(marker, goals, walls, rows, cols, canvas, cell_size)
    elif method == "BFS":
        path, node_count, directions = bfs(marker, goals, walls, rows, cols, canvas, cell_size)
    elif method == "GBFS":
        path, node_count, directions = gbfs(marker, goals, walls, rows, cols, canvas, cell_size)
    elif method == "AS":
        path, node_count, directions = a_star(marker, goals, walls, rows, cols, canvas, cell_size)
    else:
        print(f"Method '{method}' not supported.")
        return

    if path:
        # Highlight the final path in light blue
        highlight_final_path(canvas, path, cell_size)

        # Create the yellow square at the starting position
        yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)

        # Animate the yellow square along the found path
        animate_path(canvas, yellow_square, path)

        

        # Output the result in the desired format
        print(f"{method} method")
        print(f"<Node {path[-1]}> {node_count}")
        print(f"[{' , '.join(directions)}]")
    else:
        print("No path to the goal was found.")

    window.mainloop()
