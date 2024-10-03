import tkinter as tk
from grid import create_grid, create_yellow_square, animate_path
from searchstrategy import dfs

# Dictionary to map method names to their respective functions
SEARCH_METHODS = {
    "DFS": dfs
    # You can add more methods here, like "BFS": bfs, "GBFS": gbfs, etc.
}

def create_grid_window(rows, cols, marker, goals, walls, method, cell_size=50):
    """Create and display the Tkinter GUI window with the grid and animate the yellow square to the goal."""

    if method not in SEARCH_METHODS:
        print(f"Error: Search method '{method}' is not supported.")
        return

    # Select the appropriate search strategy
    search_function = SEARCH_METHODS[method]

    window = tk.Tk()
    window.title(f"Grid Visualization - {method} Search")

    # Create canvas for grid
    canvas = tk.Canvas(window, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    # Create and display the grid
    create_grid(canvas, rows, cols, markers=[marker], goals=goals, walls=walls)

    # Perform the selected search to find the path to the goal with visualized search tree
    path = search_function(marker, goals, walls, rows, cols, canvas, cell_size)

    if path:
        # Highlight the final path in light blue
        from searchstrategy import highlight_final_path
        highlight_final_path(canvas, path, cell_size)
        
        # Create the yellow square at the starting position
        yellow_square = create_yellow_square(canvas, marker[0], marker[1], cell_size)

        # Animate the yellow square along the found path
        animate_path(canvas, yellow_square, path)
    else:
        print("No path to the goal was found.")

    window.mainloop()
